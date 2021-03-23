from django.contrib import admin
from .models import GoodsType, Goods, GoodsSKU, IndexTypeGoodsBanner, IndexPromotionBanner, IndexGoodsBanner


@admin.register(GoodsType)
class GoodsTypeAdmin(admin.ModelAdmin):
    """
    商品种类模型管理器
    """
    list_display = ['name', 'logo', 'type_sales']
    list_per_page = 10


# 创建关联对象，使得在商品SPU界面可以修改商品SKU明细
class GoodsSKUTabularInline(admin.TabularInline):
    model = GoodsSKU
    extra = 2


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    """
    商品SPU类模型管理器
    """
    list_display = ['name', 'detail', 'goods_sales']
    list_per_page = 10
    # 使用此方式直接管理商品SKU表
    inlines = [GoodsSKUTabularInline]


@admin.register(GoodsSKU)
class GoodsSKUAdmin(admin.ModelAdmin):
    """
    商品详细模型类管理器
    """
    list_display = ['name', 'price', 'stock', 'sales', 'unite', 'status']
    list_per_page = 10
    search_fields = ['name']
    list_filter = ['type']    # 跨表过滤


@admin.register(IndexTypeGoodsBanner)
class IndexTypeGoodsBannerAdmin(admin.ModelAdmin):
    """
    首页分类商品展示模型类管理器
    """
    list_display = ['sku', 'type', 'display_type', 'index']
    search_fields = ['sku__name']   # search_fields 跨表查询要写清楚哦
    list_filter = ['type__name']    # list_filter   跨表过滤不需要详细说明


@admin.register(IndexPromotionBanner)
class IndexPromotionBannerAdmin(admin.ModelAdmin):
    """
    首页促销活动模型类管理器
    """
    list_display = ['name', 'index']


@admin.register(IndexGoodsBanner)
class IndexGoodsBannerAdmin(admin.ModelAdmin):
    """
    首页轮播商品模型类管理器
    """
    list_display = ['sku', 'index']