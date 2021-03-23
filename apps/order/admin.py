from django.contrib import admin
from .models import Transit, OrderInfo, OrderGoods
# Register your models here.


@admin.register(Transit)
class TransitAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderGoods)
class OrderGoodsAdmin(admin.ModelAdmin):
    pass
