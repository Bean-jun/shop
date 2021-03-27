from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django_redis import get_redis_connection
from django.db.models import Max
from apps.goods.models import GoodsSKU
from apps.order.models import Transit
from apps.user.models import Address

"""
提交订单的页面：显示用户准备购买的商品 √
点击提交订单时完成订单的创建
用户中心显示订单信息
点击支付完成支付
"""


class OrderPayView(LoginRequiredMixin, View):
    """
    订单提交视图
    """
    def post(self, request):
        user = request.user

        if not user.is_authenticated:
            return redirect(reverse('user:login'))

        # 获取数据-商品、数量、小计、总金额、收货地址、
        goods_id = request.POST.getlist('goods_id')
        if not goods_id:
            return redirect(reverse('cart:show'))

        address = Address.objects.filter(user=user)


        client = get_redis_connection('default')
        key = 'user_cart_%d' % user.id

        skus = []
        # 总金额和总件数
        total_amount = 0
        total_count = 0

        for id in goods_id:
            sku = GoodsSKU.objects.get(id=id)
            goods_num = client.hget(key, id).decode()

            setattr(sku, 'goods_num', goods_num)
            setattr(sku, 'amount', sku.price*int(goods_num))

            skus.append(sku)

            total_count += int(goods_num)
            total_amount += sku.price*int(goods_num)

        if total_amount < Transit.objects.aggregate(Max('transit')).get('transit__max'):
            transit = 10
        else:
            transit = 0

        total_pay = total_amount + transit


        # 返回应答
        context = {
            'skus': skus,
            'total_amount': total_amount,
            'total_count': total_count,
            'address': address,
            'transit': transit,
            'total_pay': total_pay,
        }
        return render(request, 'order/place_order.html', context)