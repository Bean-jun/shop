from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from apps.user.models import User
from django.urls import reverse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout


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
        send_content = f"""欢迎您{user.username},恭喜您成为本商城会员🤣.<br />
                        请点击以下链接完成账户激活<br />
                        <a href="http:{settings.WEB_ADDRESS}:{settings.WEB_HOST}/user/activate/{token}">
                        http:{settings.WEB_ADDRESS}:{settings.WEB_HOST}/user/activate/{token}</a>"""

        # 发送邮件
        subject = "购物商城欢迎您"
        send_mail(subject=subject,
                  message='',
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[email],
                  html_message=send_content)

        # 返回应答
        # todo: 注意goods路由配置的的命名
        return HttpResponse("register")
        # return redirect(reverse('goods:index'))


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
                # todo : 注意账号登录路由配置的命名
                return HttpResponse('activate')
                # return redirect(reverse('user:login'))


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

        response = HttpResponse("login")

        if user is not None:
            # 设置cookie
            if allow == 'on':
                response.set_cookie('username', username, expires=7*60*60)
            else:
                response.delete_cookie('username')

            login(request, user)

        # 返回应答
        return HttpResponse("login")


class LogoutView(View):
    """
    用户退出
    """
    def get(self, request):
        logout(request)
        return HttpResponse("logout")