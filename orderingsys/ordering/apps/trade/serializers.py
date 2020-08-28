import time
import json
from rest_framework import serializers
from django.forms import model_to_dict
from rest_framework.exceptions import ValidationError

from trade import models
from users.models import UserInfo
from users.serializers import UserInfoSerializers
from food.serializers import FoodSerializers

class TradeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model =  models.ShoppingCart
        exclude = ['user','add_time']

    def create(self, validated_data):
        nums = validated_data["nums"]
        food = validated_data["food"]

        existed = models.ShoppingCart.objects.filter(food=food)
        # 判断当前是否已有记录
        if existed:
            existed = existed[0]
            existed.nums = nums
            existed.save()
        else:
            existed = models.ShoppingCart.objects.create(**validated_data)
        # 需要返回保存数据
        return existed
    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance

class ShopCartDetailSerializer(serializers.Serializer):
    '''
    购物车商品详情信息
    '''
    # 一个购物车对应一个商品
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.FloatField()
    yun_price = serializers.FloatField()
    courier_type = serializers.CharField()
    status = serializers.IntegerField()
    food_image = serializers.ImageField()
    nums = serializers.SerializerMethodField()

    def get_nums(self,obj):
        token = self.context['request'].META.get('HTTP_AUTHORIZATION', None)
        user_object = models.UserInfo.objects.filter(token=token).first()
        detail_queryset = models.ShoppingCart.objects.filter(user = user_object)
        return [model_to_dict(row,fields=['nums',]) for row in detail_queryset ]

class OrderSerializer(serializers.ModelSerializer):
    #生成订单的时候这些不用post
    pay_status = serializers.CharField(read_only=True,source='get_order_status_display')
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    nonce_str = serializers.CharField(read_only=True)
    pay_type = serializers.CharField(read_only=True)

    class Meta:
        model = models.OrderInfo
        exclude = ['user','add_time']

class OrderInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=True,max_length=30)
    price = serializers.IntegerField()
    status = serializers.IntegerField()
    food_image = serializers.ImageField()
    nums = serializers.SerializerMethodField()
    yun_price = serializers.IntegerField()
    courier_type = serializers.CharField()
    userAddress = serializers.SerializerMethodField()

    def get_nums(self,obj):
        food_lists = json.loads(self.context['request'].query_params.get("goods"))
        if len(food_lists)==1:
            return [{'nums':row['nums'] for row in food_lists }]
        token = self.context['request'].META.get('HTTP_AUTHORIZATION', None)
        user_object = models.UserInfo.objects.filter(token=token).first()
        detail_queryset = models.ShoppingCart.objects.filter(user = user_object)
        return [model_to_dict(row,fields=['nums',]) for row in detail_queryset ]

    def get_userAddress(self,obj):
        token = self.context['request'].META.get('HTTP_AUTHORIZATION', None)
        user_object = models.UserInfo.objects.filter(token=token).first()
        detail_queryset = models.Address.objects.filter(user = user_object,is_default = True)
        return [model_to_dict(row,exclude = ['province_id','add_time','city_id','area_id','is_default',]) for row in detail_queryset ]

class TradeOrderListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order_sn = serializers.CharField()
    order_mount = serializers.FloatField()
    post_script = serializers.CharField()
    orderinfo_status = serializers.IntegerField()
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    image = serializers.SerializerMethodField()

    def get_image(self,obj):
        food_queryset = models.OrderFoods.objects.filter(order = obj)
        food_image_list = models.Food.objects.filter(id__in =  [row.food.id for row in food_queryset])
        ser = FoodSerializers(food_image_list, many=True, context=self.context)
        image = []
        for item in  ser.data:
            image_dict = {}
            image_dict['id'] = item['id']
            image_dict['image'] = item['food_image']
            image.append(image_dict)
        return image
