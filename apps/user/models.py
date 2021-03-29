from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.BaseModel import BaseModel


class User(AbstractUser, BaseModel):
    """
    用户模型类
    """
    image = models.ImageField(upload_to="user_image", verbose_name="用户头像")

    class Meta:
        db_table = "shop_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    
class Address(BaseModel):
    """
    用户地址模型类
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="所属账户")    # on_delete=models.CASCADE 删除关联数据,与之关联也删除
    receiver = models.CharField(max_length=20, verbose_name="收件人")
    phone = models.CharField(max_length=11, verbose_name="手机号码")
    addr = models.CharField(max_length=30, verbose_name="收件地址")
    zip_code = models.CharField(max_length=6, default="000000", verbose_name="邮编")
    is_default = models.BooleanField(default=False, verbose_name="是否默认")

    class Meta:
        db_table = "shop_address"
        verbose_name = "地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.addr
        