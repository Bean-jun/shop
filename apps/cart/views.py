from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django_redis import get_redis_connection

from apps.goods.models import GoodsSKU
from utils.CartShow import CartInfoShow

"""
列表页和详情页可以将商品添加到购物车 √
用户登录后，首页、详细页、列表页显示登录用户购物车中的商品数量 √
购物车页面：对用户购物车的操作，入选择某种商品，增加、减少商品等等 √
"""


class CartInfoView(View):
    """
    购物车视图
    """
    def get(self, request):
        # 获取数据
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse("user:login"))

        client = get_redis_connection('default')
        key = 'user_cart_%d' % user.id
        res_dict = client.hgetall(key)

        # 获取购物车中商品件数
        try:
            cart_count = CartInfoShow()(user.id)
        except:
            cart_count = 0

        # 计算总金额和总件数
        amount_price = 0
        amount_count = 0

        goods_content = []
        for goods_id, count in res_dict.items():
            goods = GoodsSKU.objects.get(id=goods_id)

            # 动态增加数量
            setattr(goods, 'count', count.decode())
            setattr(goods, 'amount', goods.price * int(count.decode()))

            goods_content.append(goods)

            amount_count += int(count.decode())
            amount_price += goods.price * int(count.decode())

        # 返回应答
        context = {
            'goods_content': goods_content,
            'cart_count': cart_count,
            'amount_price': amount_price,
            'amount_count': amount_count,
        }

        return render(request, 'cart/cart.html', context)


class CartAddView(View):
    """
    购物车添加视图
    """
    def post(self, request):

        # 校验用户登录问题
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse('user:login'))

        # 获取数据
        goods_id = request.POST.get('goods_id')
        count = request.POST.get('count')

        # 校验数据
        if not all([goods_id, count]):
            return JsonResponse({'msg': 'error'})

        try:
           sku = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'msg': 'error_not_found'})

        # 大于库存
        if sku.stock < int(count):
            return JsonResponse({'msg': "error_stock_not_enough"})

        # 添加购物车, 使用hash表存储
        client = get_redis_connection('default')
        key = 'user_cart_%d' % user.id
        # 商品存在，就添加相关的数量
        if client.hexists(key, sku.id):
            # 存在即直接添加count个数量
            client.hincrby(key, sku.id, count)
        else:
            # 商品不存在，直接添加商品内容
            client.hset(key, sku.id, count)

        # 返回应答
        return JsonResponse({'msg': 'ok'})


class CartDeleteView(View):
    """
    购物车删除视图
    """
    def post(self, request):
        # 获取数据
        user = request.user
        goods_id = request.POST.get('goods_id')


        client = get_redis_connection('default')
        key = 'user_cart_%d' % user.id

        # 商品存在，就删除
        if client.hexists(key, goods_id):
            client.hdel(key, goods_id)

        return JsonResponse({'msg': 'ok'})



class CartUpdateView(View):
    """
    购物车修改视图
    """
    def post(self, request):
        # 获取数据
        user = request.user
        goods_id = request.POST.get('goods_id')
        count = request.POST.get('count')

        # 校验数据
        if not all([goods_id, count]):
            return JsonResponse({'msg': 'error'})

        try:
           sku = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'msg': 'error_not_found'})

        # 大于库存
        if sku.stock < int(count):
            return JsonResponse({'msg': "error_stock_not_enough"})

        client = get_redis_connection('default')
        key = 'user_cart_%d' % user.id

        client.hset(key, sku.id, count)

        return JsonResponse({'msg': 'ok'})
