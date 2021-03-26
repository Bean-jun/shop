from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View


class OrderPayView(LoginRequiredMixin, View):
    """
    订单提交视图
    """
    def post(self, request):
        return render(request, 'order/place_order.html')