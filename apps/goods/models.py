from django.db import models
from utils.BaseModel import BaseModel
from django.db.models import Sum
from ckeditor.fields import RichTextField


class GoodsType(BaseModel):
    """
    商品类型模型类
    """
    name = models.CharField(max_length=100, verbose_name='种类名称')
    logo = models.CharField(max_length=100, verbose_name='标识')
    image = models.ImageField(upload_to='type', verbose_name='商品类型图片')

    class Meta:
        db_table = 'shop_goods_type'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def type_sales(self):
        # SPU模型商品总销量
        res = GoodsSKU.count_sales(goods_type=self.name)
        return res

    type_sales.short_description = "销量"


class Goods(BaseModel):
    """
    商品SPU模型类
    """
    name = models.CharField(max_length=100, verbose_name='商品SPU名称')
    # detail = models.CharField(max_length=200, blank=True, verbose_name='商品详情')
    # 添加富文本编辑器
    detail = RichTextField(blank=True, verbose_name='商品详情')

    def goods_sales(self):
        # SPU模型商品总销量
        res = GoodsSKU.count_sales(goods_name=self.name)
        return res

    class Meta:
        db_table = 'shop_goods'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    goods_sales.short_description = "销量"


class GoodsSKU(BaseModel):
    """
    商品SKU模型类 -- 商品详细明细表
    """
    STATUS = (
        (0, '下架'),
        (1, '上架')
    )
    type = models.ForeignKey('GoodsType', on_delete=models.CASCADE, verbose_name='商品种类')
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='商品SPU')
    name = models.CharField(max_length=100, verbose_name='商品名称')
    desc = models.CharField(max_length=200, verbose_name='商品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    unite = models.CharField(max_length=100, verbose_name='商品单位')
    image = models.ImageField(upload_to='goods', verbose_name='商品图片')
    stock = models.IntegerField(default=1, verbose_name='商品库存')
    sales = models.IntegerField(default=0, verbose_name='商品销量')
    status = models.SmallIntegerField(default=1, choices=STATUS, verbose_name='商品状态')

    class Meta:
        db_table = 'shop_goods_sku'
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @classmethod
    def count_sales(cls, goods_type=None, goods_name=None):
        # type种类的商品总销量， SPU的商品总销量
        if any([goods_type, goods_name]):
            if goods_type is None:
                # 返回SPU的商品总销量
                res = GoodsSKU.objects.filter(goods__name=goods_name).aggregate(Sum('sales')).get('sales__sum')
            elif goods_name is None:
                # 返回type种类的商品总销量
                res = GoodsSKU.objects.filter(type__name=goods_type).aggregate(Sum('sales')).get('sales__sum')
        else:
            res = 0
        return res


class GoodsImage(BaseModel):
    """
    商品图片模型类
    """
    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE, verbose_name='商品')
    image = models.ImageField(upload_to='goods', verbose_name='图片路径')

    class Meta:
        db_table = 'shop_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name


class IndexGoodsBanner(BaseModel):
    """
    首页轮播商品展示模型类
    """
    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE, verbose_name='商品')
    image = models.ImageField(upload_to='banner', verbose_name='图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'shop_index_banner'
        verbose_name = '首页轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sku.name


class IndexTypeGoodsBanner(BaseModel):
    """
    首页分类商品展示模型类
    """
    DISPLAY_TYPE_CHOICES = (
        (0, '标题'),
        (1, '图片')
    )
    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE, verbose_name='商品SKU')
    type = models.ForeignKey('GoodsType', on_delete=models.CASCADE, verbose_name='商品种类')
    display_type = models.SmallIntegerField(default=0, choices=DISPLAY_TYPE_CHOICES, verbose_name='展示类型')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'shop_index_type_goods'
        verbose_name = '主页分类展示商品'
        verbose_name_plural = verbose_name


class IndexPromotionBanner(BaseModel):
    """
    首页促销活动模型类
    """
    name = models.CharField(max_length=20, verbose_name='活动名称')
    url = models.URLField(verbose_name='活动链接')
    image = models.ImageField(upload_to='banner', verbose_name='活动图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'shop_index_promotion'
        verbose_name = '主页促销活动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
