from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View

from apps.goods.models import GoodsType, IndexTypeGoodsBanner, IndexPromotionBanner, IndexGoodsBanner, GoodsSKU, Goods

"""
首页
    动态指定首页轮播商品信息 √
    动态指定首页活动信息 √
    动态获取商品的种类信息并显示 √
    动态指定首页显示的每个种类的商品 √
    点击某一个商品时跳转到商品的详情页面 √
商品详情页
    显示出某个商品的详情信息 √
    页面的左下方显示出该种类商品的2个新品信息 √
商品列表页
    显示出某一类商品的列表数据，分页显示并支持默认、价格、人气排序
    页面的左下方显示该种商品的2个新品信息
    通过页面搜索框查询商品信息
"""


class IndexView(View):
    """
    首页
    """
    def get(self, request):
        # 获取分类商品
        try:
            goods_type = GoodsType.objects.all()
        except GoodsType.DoesNotExist:
            goods_type = None

        if goods_type is not None:
            # 获取对应的种类的SKU商品
            for good_type in goods_type:
                # 获取标题类型商品
                title_banners = IndexTypeGoodsBanner.objects.filter(type=good_type, display_type=0)
                # 获取图片类型商品
                image_banners = IndexTypeGoodsBanner.objects.filter(type=good_type, display_type=1)

                # 设置good_type属性
                setattr(good_type, 'title_banners', title_banners)
                setattr(good_type, 'image_banners', image_banners)

        # 获取首页促销活动
        promotion_banners = IndexPromotionBanner.objects.all()

        # 获取首页轮播商品
        goods_banners = IndexGoodsBanner.objects.all()

        context = {
            'goods_type': goods_type,
            'promotion_banners': promotion_banners,
            'goods_banners': goods_banners,
        }
        # 返回首页
        return render(request, 'goods/index.html', context)


class DetailView(View):
    """
    商品详情页
    """
    def get(self, request, goods_id):
        # 获取单品信息
        try:
            goods = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            return redirect(reverse('goods:index'))

        # 获取单品同spu信息
        skus = GoodsSKU.objects.filter(goods_id=goods.goods)

        # 获取新品信息
        try:
            new_goods = GoodsSKU.objects.filter(type=goods.type).exclude(goods=goods.goods)[:2]
        except GoodsSKU.DoesNotExist:
            new_goods = None

        # 获取商品总类型信息
        goods_type = GoodsType.objects.all()

        context = {
            'goods': goods,
            'new_goods': new_goods,
            'goods_type': goods_type,
            'skus': skus,
        }
        # 返回详情页
        return render(request, 'goods/detail.html', context)