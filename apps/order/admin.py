from django.contrib import admin
from .models import Transit, OrderInfo, OrderGoods
# Register your models here.


@admin.register(Transit)
class TransitAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'addr', 'pay_method', 'total_price', 'total_count', 'order_status', 'order_pay_id']


@admin.register(OrderGoods)
class OrderGoodsAdmin(admin.ModelAdmin):
    pass
