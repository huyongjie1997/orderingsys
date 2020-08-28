from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField

from users.models import UserInfo

# Create your models here.
class FoodCategory(models.Model):
    """
    商品类别
    """
    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "菜品类别"
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.name

class Food(models.Model):
    COURIER_TYPE = (
        ("顺丰快递", "15.00.00"),
        ("圆通快递", "10.00"),
        ("韵达快递", "8.00"),
        ("京东快递", "15.00"),
        ("邮政快递", "6.00"),
        ("包邮", "0.00"),
    )
    foodcategory = models.ForeignKey(FoodCategory,on_delete=models.CASCADE, verbose_name="菜品类别", related_name="foodcategory")
    name = models.CharField(max_length=100, verbose_name="菜名")
    comment_count = models.IntegerField(default=0, verbose_name="评论数")
    month_count = models.IntegerField(default=0, verbose_name="月销售量")
    status = models.IntegerField(default=0, verbose_name="库存数")
    price = models.FloatField(default=0.00, verbose_name="价格")
    yun_price = models.FloatField(default=0.00, verbose_name="运费")
    courier_type = models.CharField("快递类型",choices=COURIER_TYPE, default="包邮", max_length=10)
    summary = UEditorField(verbose_name="介绍", imagePath="food/images/", width=1000, height=300,toolbars='full',filePath="goods/files/",upload_settings={'imageMaxSizing':1024000}, default='',settings={}, command=None)
    food_image = models.ImageField(upload_to="food/images/", null=True, blank=True, verbose_name="封面图")
    created_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '菜名'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class FoodDetailsImage(models.Model):
    food = models.ForeignKey(Food,on_delete=models.CASCADE, verbose_name="菜品名", related_name="food")
    food_detail_image = models.ImageField(upload_to="food/images/", null=True, blank=True, verbose_name="菜品详细图")
    created_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '菜品详细图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.food.name

class FoodComment(models.Model):

    COMMENT_TYPE = (
        ("praise", "好评"),
        ("mid-review", "中评"),
        ("bad", "差评"),
    )
    food = models.ForeignKey(Food,on_delete=models.CASCADE, verbose_name="菜品名", related_name="foodcomment")
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE, verbose_name="用户评论", related_name="usercomment")
    comment = models.CharField(max_length=100, verbose_name="评论内容")
    comment_type = models.CharField("评论等级",choices=COMMENT_TYPE, default="praise", max_length=10)
    created_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment_type