from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django_redis import get_redis_connection
from django.db.models import Max
from apps.goods.models import GoodsSKU
from apps.order.models import Transit, OrderInfo, OrderGoods
from apps.user.models import Address
from django.db import transaction
from django.conf import settings
from django.utils.decorators import method_decorator    # 对类进行装饰
from django.views.decorators.csrf import csrf_exempt
from apps.order.Payment.PaymentByAlipay import AliPayment


"""
提交订单的页面：显示用户准备购买的商品 √
点击提交订单时完成订单的创建 √
用户中心显示订单信息 √
点击支付完成支付 √
"""


class OrderPlaceView(LoginRequiredMixin, View):
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
            setattr(sku, 'amount', sku.price * int(goods_num))

            skus.append(sku)

            total_count += int(goods_num)
            total_amount += sku.price * int(goods_num)

        max_transit = Transit.objects.aggregate(Max('transit')).get('transit__max')
        if total_amount < max_transit:
            transit = Transit.objects.get(transit=max_transit)
        else:
            transit = Transit.objects.get(transit=0)

        total_pay = total_amount + transit.transit

        # 返回应答
        context = {
            'skus': skus,
            'total_amount': total_amount,
            'total_count': total_count,
            'address': address,
            'transit': transit,
            'total_pay': total_pay,
            'goods_id': goods_id,
        }
        return render(request, 'order/place_order.html', context)


class OrderCreateView(View):
    """
    订单创建
    """

    @transaction.atomic
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse('user:login'))

        # 接收参数
        addr = request.POST.get('addr')
        pay_method = request.POST.get('pay_method')
        goods_ids = request.POST.get('goods_ids')
        transit_id = request.POST.get('transit_id')

        # 校验数据
        if not all([addr, pay_method, goods_ids, transit_id]):
            return JsonResponse({'msg': 'error'})

        # 地址
        try:
            address = Address.objects.get(id=addr)
        except Address.DoesNotExist:
            return JsonResponse({'msg': "地址错误"})

        # 支付方式
        try:
            if int(pay_method) not in dict(OrderInfo.PAY_METHOD).keys():
                return JsonResponse({'msg': '支付方式错误'})
        except Exception as e:
            return JsonResponse({'msg': '支付参数错误'})

        # 邮费
        try:
            transit = Transit.objects.get(id=transit_id)
        except Exception as e:
            return JsonResponse({'msg': '邮费参数错误'})

        # 创建事务保存点
        save_point = transaction.savepoint()

        # 创建订单
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        # 总金额
        total_price = 0
        # 总件数
        total_count = 0

        # 提交订单
        try:
            order = OrderInfo.objects.create(order_id=order_id,
                                             user=user,
                                             addr=address,
                                             transit_price=transit,
                                             pay_method=pay_method,
                                             total_count=total_count,
                                             total_price=total_price,
                                             )
            # 获取商品数量及总金额
            client = get_redis_connection('default')
            key = 'user_cart_%d' % user.id

            for goods_id in eval(goods_ids):
                try:
                    sku = GoodsSKU.objects.select_for_update().get(id=goods_id)
                except Exception as e:
                    transaction.savepoint_rollback(save_point)
                    return JsonResponse({'msg': "商品不存在"})

                # 获取用户需要的数量
                count = client.hget(key, goods_id).decode()

                if int(count) > sku.stock:
                    transaction.savepoint_rollback(save_point)
                    return JsonResponse({'msg': "库存不足"})

                OrderGoods.objects.create(order=order,
                                          sku=sku,
                                          count=count,
                                          price=sku.price)

                # 仓库商品变动
                sku.stock -= int(count)
                sku.sales += int(count)
                sku.save()

                # 总件数及总总金额处理
                total_count += int(count)
                total_price += sku.price * int(count)

            # 处理总金额及件数
            order.total_count = total_count
            order.total_price = total_price
            order.save()
        except Exception as e:
            print(e.args)
            # 回滚数据
            transaction.savepoint_rollback(save_point)
            return JsonResponse({'msg': '订单商品失败'})
        else:
            # 提交数据
            transaction.savepoint_commit(save_point)

            # 清除购物车
            client.hdel(key, *eval(goods_ids))

        # 返回应答
        return JsonResponse({'msg': 'ok'})


class OrderPayView(View):
    """
    用户支付
    """
    def post(self, request):
        # 获取数据内容
        order_id = request.POST.get('order_id')

        try:
            order = OrderInfo.objects.get(order_id=order_id)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'msg': '订单不存在'})

        if order.order_status == 1:
            # 订单未交易成功
            if order.pay_method == 1:
                # 支付宝接口调用
                callback_url = 'http://' + settings.WEB_ADDRESS + ':' + settings.WEB_HOST + reverse('order:update')
                payment = AliPayment(appid=settings.APPID)
                pay_url = payment.get_pay(order.order_id,
                                          order.total_price,
                                          order.order_id,
                                          return_url=callback_url,
                                          notify_url=callback_url
                                          )

                return JsonResponse({'msg': 1000, 'url': pay_url})

            elif order.pay_method == 2:
                # 微信接口调用
                return JsonResponse({'msg': '接口调用完善中'})

            elif order.pay_method == 3:
                # 银行卡接口调用
                return JsonResponse({'msg': '接口调用完善中'})
        else:
            return JsonResponse({'msg': '支付成功,其他接口完善中...'})


@method_decorator(csrf_exempt, name='dispatch')     # 避免支付宝notify_url异步post请求被中间件阻止
class OrderUpdateView(View):
    """
    订单数据更新
    """

    def get(self, request):
        '''
        支付宝中return_url=None对应跳转请求
        '''
        # TODO：部署上线时，这部分代码应该注释掉，仅仅保留return部分
        params = request.GET.dict()
        signature = params.pop("sign")
        payment = AliPayment(appid=settings.APPID)
        try:
            status = payment.get_res(params, signature)
        except Exception as e:
            status = False

        # 校验支付结果
        if status == True:
            # 处理后台数据
            order_id = params.get('out_trade_no', None)
            trade_no = params.get('trade_no', None)
            try:
                order = OrderInfo.objects.get(order_id=order_id)
            except OrderInfo.DoesNotExist:
                pass
            else:
                order.order_status = 2
                order.order_pay_id = trade_no
                order.save()

        # 返回应答
        return redirect(reverse('user:order', args=(1,)))

    def post(self, request):
        '''
        支付宝中 notify_url=None对应跳转请求
        post方式
        返回值为success时，支付宝才不会一直发生请求回传数据
        该部分需要使用公网IP地址
        '''
        params = request.POST.dict()
        signature = params.pop("sign")
        payment = AliPayment(appid=settings.APPID)
        try:
            status = payment.get_res(params, signature)
        except Exception as e:
            status = False

        # 校验支付结果
        if status == True:
            # 处理后台数据
            order_id = params.get('out_trade_no', None)
            trade_no = params.get('trade_no', None)
            try:
                order = OrderInfo.objects.get(order_id=order_id)
            except OrderInfo.DoesNotExist:
                pass
            else:
                order.order_status = 2
                order.order_pay_id = trade_no
                order.save()

        # 给支付宝返回应答
        return HttpResponse('success')
