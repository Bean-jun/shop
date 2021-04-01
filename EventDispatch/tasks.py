import os
from django.core.mail import send_mail
from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')


app = Celery('EventDispatch.tasks', broker=settings.CELERY_ADDRESS)


@app.task()
def user_register_mail(username, email, token):
    '''
    邮件激活
    :param email: 用户邮箱
    :param username: 用户
    :param token: 用户唯一标识码
    :return: None
    '''
    send_content = f"""欢迎您{username},恭喜您成为本商城会员🤣.<br />
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
