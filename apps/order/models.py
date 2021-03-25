from django.db import models
from utils.BaseModel import BaseModel


class Transit(BaseModel):
    """
    运费模型类
    """
    TRANSIT_PRICE = (
        (0, '包邮'),
        (10, '不包邮'),
    )
    transit = models.SmallIntegerField(choices=TRANSIT_PRICE, verbose_name="运费")

    def __str__(self):
        return str(self.transit)

    class Meta:
        verbose_name = '运费'
        verbose_name_plural = verbose_name


class OrderInfo(BaseModel):
    """
    订单信息模型类
    """
    PAY_METHOD = (
        (1, "支付宝"),
        (2, "微信"),
        (3, "银行卡"),
    )
    PAY_STATUS = (
        (1, "待支付"),
        (2, "待发货"),
        (3, "已发货"),
        (4, "待评价"),
        (5, "已评价"),
    )
    order_id = models.CharField(max_length=128, primary_key=True, verbose_name="订单号")
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name='用户')
    addr = models.ForeignKey("user.Address", on_delete=models.CASCADE, verbose_name='地址')
    transit_price = models.ForeignKey('Transit', on_delete=models.CASCADE, verbose_name="运费")
    pay_method = models.SmallIntegerField(choices=PAY_METHOD, verbose_name="支付方式")
    total_count = models.IntegerField(default=1, verbose_name="商品数目")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品价格")
    order_status = models.SmallIntegerField(choices=PAY_STATUS, default=1, verbose_name="订单状态")
    order_pay_id = models.CharField(max_length=128, default="", verbose_name="支付编号")

    class Meta:
        db_table = "shop_order_info"
        verbose_name = "订单"
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    """
    订单商品模型类
    """
    order = models.ForeignKey('OrderInfo', on_delete=models.CASCADE, verbose_name="订单")
    sku = models.ForeignKey('goods.GoodsSKU', on_delete=models.CASCADE, verbose_name="商品SKU")
    count = models.IntegerField(default=1, verbose_name="商品数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品价格")
    comment = models.TextField(verbose_name="评论")

    class Meta:
        db_table = "shop_order_goods"
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name
