from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django_redis import get_redis_connection

from apps.goods.models import GoodsSKU
from apps.order.models import OrderInfo, OrderGoods
from apps.user.models import User, Address
from django.urls import reverse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin   # 对未登录账户限制访问
from EventDispatch.tasks import user_register_mail


"""
注册
    注册时校验用户是否已经被注册 √
    完成用户的注册 √
    在注册时，需要给用户发送激活链接，让用户点击链接从而完成账户激活 √
登录
    实现用户的登录及退出 √
用户中心
    用户信息页：显示用户的信息，包括用户名、电话和收货地址 √  用户最近浏览的商品记录 √
    用户地址页：显示用户的默认收货地址，页面下方同时可以增加用户的收货地址 √
    用户订单页：显示用户的订单信息 √
其他
    待补充
"""


class RegisterView(View):
    """
    用户注册
    """

    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        # 获取数据
        res = request.POST
        username = res.get('user_name')
        password = res.get('pwd')
        password_ = res.get('cpwd')
        email = res.get('email')
        allow = res.get('allow')

        # 校验数据
        # 完整性
        if not all([username, password, password_, email]):
            return render(request, 'user/register.html', {'error': '内容缺少'})

        # 密码校验
        if password != password_:
            return render(request, 'user/register.html', {'error': '密码不一致'})

        # 协议校验
        if allow != 'on':
            return render(request, 'user/register.html', {'error': '请同意协议'})

        # 重复注册校验
        try:
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            user = None

        # 账户可能注册过，但是激活失败了
        if user:
            if user.is_active == 1:
                return render(request, 'user/register.html', {'error': '请不要重复注册'})
            else:
                return render(request, 'user/register.html', {'error': '请联系管理员激活账号'})
        else:
            # 创建用户
            user = User.objects.create_user(username=username, email=email, password=password)

            # 初始为激活账户
            user.is_active = 0
            user.save()

        # 邮箱激活
        # 产生秘钥
        res = Serializer(secret_key=settings.SECRET_KEY, expires_in=20 * 60)
        token = res.dumps({'id': user.id, 'username': user.username}).decode()

        # 发送邮件
        user_register_mail(user, token).delay()

        # 返回应答
        return redirect(reverse('user:login'))


class ActivateView(View):
    """
    邮件激活
    """

    def get(self, request, token):
        # 获取激活邮件激活账户
        res = Serializer(secret_key=settings.SECRET_KEY)
        token = res.loads(token)
        try:
            user_id = token.get('id')
            username = token.get('username')
        except SignatureExpired:
            return HttpResponse("激活链接已经失效")
        else:
            # 校验账号id和用户名
            try:
                user = User.objects.get(id=user_id, username=username)
            except User.DoesNotExist:
                # 不存在就直接让用户去注册
                return redirect(reverse('user:register'))
            else:
                user.is_active = 1
                user.save()
                return redirect(reverse('user:login'))


class LoginView(View):
    """
    用户登录界面
    """

    def get(self, request):
        # 获取用户内容
        username = request.COOKIES.get('username')
        return render(request, 'user/login.html', {'username': username})

    def post(self, request):
        # 获取数据
        res = request.POST
        username = res.get('username')
        password = res.get('pwd')
        allow = res.get('allow')

        # 验证数据
        if not all([username, password]):
            return render(request, 'user/login.html', {'error': "数据不完整"})

        # 登录处理
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active == 1:

                # 登录
                login(request, user)

                # 获取未登录账户登录后的跳转页
                next_url = request.GET.get('next', reverse('goods:index'))

                response = redirect(next_url)

                # 设置cookie
                if allow == 'on':
                    response.set_cookie('username', username, expires=7*60*60)
                else:
                    response.delete_cookie('username')

                # 返回应答
                return response
            else:
                return render(request, 'user/register.html', {'error': '请联系管理员激活账号'})
        else:
            # 数据不正确
            return redirect(reverse('user:register'))


class LogoutView(View):
    """
    用户退出
    """
    def get(self, request):
        logout(request)
        return redirect(reverse('goods:index'))


class UserInfoView(LoginRequiredMixin, View):
    """
    用户信息页
    """
    def get(self, request):
        # 个人信息获取
        user = request.user
        try:
            address = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
            address = None

        # 浏览记录获取
        user = request.user
        goods_id = []
        if user.is_authenticated:
            client = get_redis_connection('default')
            key = 'user_use_history_%d' % user.id
            goods_id = client.lrange(key, 0, 4)

        # 获取用户浏览记录商品信息
        user_show_goods = []
        for i in goods_id:
            sku = GoodsSKU.objects.get(id=i)
            user_show_goods.append(sku)

        # 组织内容
        context = {
            'address': address,
            'active': True,
            'user_show_goods': user_show_goods,
        }

        return render(request, 'user/user_center_info.html', context)


class UserSiteView(LoginRequiredMixin, View):
    """
    用户地址页
    """
    def get(self, request):

        # 获取用户收货地址
        user = request.user
        try:
            address = Address.objects.filter(user=user)
        except Address.DoesNotExist:
            address = None

        context = {
            'address': address,
            'active': True,
        }
        return render(request, 'user/user_center_site.html', context)

    def post(self, request):
        # 获取数据
        res = request.POST
        user = request.user
        receiver = res.get('receiver')
        addr = res.get('addr')
        zip_code = res.get('zip_code')
        phone = res.get('phone')
        is_default = False

        # 校验数据
        if not all([receiver, addr, phone]):
            return render(request, 'user/user_center_site.html', {'error': "数据不完整"})

        # 业务处理
        # 避免重复添加
        try:
            Address.objects.get(user=user,
                                receiver=receiver,
                                phone=phone,
                                addr=addr)
        except Address.DoesNotExist:
            # 不存在就添加地址
            address = Address.objects.create(user=user,
                                             receiver=receiver,
                                             phone=phone,
                                             addr=addr,
                                             zip_code=zip_code)

            # 查询是否存在默认地址
            try:
                Address.objects.filter(user=user).filter(is_default=True)
            except Address.DoesNotExist:
                # 不存在默认收货地址
                is_default = True

            address.is_default = is_default
            address.save()

        # 返回应答
        return redirect(reverse('user:site'))


class UserOrderView(LoginRequiredMixin, View):
    """
    用户订单页
    """
    def get(self, request, page):
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse('user:login'))

        # 获取订单内容
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')


        for order in orders:

            order_goods = OrderGoods.objects.filter(order=order)

            for goods in order_goods:
                amount = goods.price * goods.count

                setattr(goods, 'amount', amount)

            setattr(order, 'order_goods', order_goods)
            setattr(order, 'status', dict(OrderInfo.PAY_STATUS)[order.pay_method])

        # 分页显示
        paginator = Paginator(orders, 4)

        try:
            page = int(page)
        except:
            page = 1

        try:
            orders = paginator.page(page)
        except Exception as e:
            orders = paginator.page(1)

        # 获取总页数
        num_pages = paginator.num_pages
        if num_pages < 5:
            page_nums = range(1, num_pages + 1)
        elif page <= 3:
            page_nums = range(1, 6)
        elif num_pages - page <= 2:
            page_nums = range(num_pages - 3, num_pages + 1)
        else:
            page_nums = range(page - 2, page + 3)

        # 组织内容
        context = {
            'orders': orders,
            'page_nums': page_nums,
            'active': True,
        }
        return render(request, 'user/user_center_order.html', context)