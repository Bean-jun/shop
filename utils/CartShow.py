from django_redis import get_redis_connection


class CartInfoShow():
    """
    首页、列表页、详细页购物车数量显示
    """
    def __call__(self, user_id):
        client = get_redis_connection('default')
        key = 'user_cart_%d' % user_id
        return client.hlen(key)