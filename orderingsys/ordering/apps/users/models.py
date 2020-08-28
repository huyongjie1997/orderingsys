from django.db import models
from datetime import datetime

# Create your models here.
class UserInfo(models.Model):
    phone = models.CharField(verbose_name='手机号', max_length=11)
    nickname = models.CharField(verbose_name='昵称', max_length=64)
    avatar = models.CharField(verbose_name='头像', max_length=200, null=True,blank=True)
    token = models.CharField(verbose_name='用户Token', max_length=64,null=True,blank=True)
    revenue = models.IntegerField(verbose_name='用户金额', default=0)
    balance = models.IntegerField(verbose_name='用户余额', default=0)
    class Meta:
        verbose_name = u"用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname

class Address(models.Model):
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE, verbose_name="用户")
    address = models.CharField(max_length=100, default="", verbose_name="详细地址")
    province_id =  models.IntegerField(verbose_name='省份id', null=True, blank=True)
    province_str = models.CharField(max_length=100, null=True, blank=True, verbose_name="省份")
    city_id =  models.IntegerField(verbose_name='城市id', null=True, blank=True)
    city_str = models.CharField(max_length=100, null=True, blank=True, verbose_name="城市")
    area_id =  models.IntegerField(verbose_name='地区id', null=True, blank=True)
    area_str = models.CharField(max_length=100, null=True, blank=True, verbose_name="地区")
    signer_name = models.CharField(max_length=20, default="", verbose_name="签收人")
    is_default = models.BooleanField(default=False, verbose_name="是否默认地址")
    singer_mobile = models.CharField(max_length=11, verbose_name="联系电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"用户地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.nickname

