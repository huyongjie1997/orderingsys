
from rest_framework import serializers
from django.forms import model_to_dict
from django.db.models import Q

from food import models
from users.serializers import UserInfoSerializers
from trade.models import ShoppingCart


class IndexSerializers(serializers.ModelSerializer):
    food = serializers.SerializerMethodField()
    image_list =  serializers.SerializerMethodField()
    # name = serializers.SerializerMethodField()
    class Meta:
        model =  models.FoodCategory
        fields = ['food','image_list']
    def get_food(self, obj):
        item_object_list = models.Food.objects.all()
        ser = FoodSerializers(instance=item_object_list, many=True, context=self.context)
        return ser.data

    def get_image_list(self, obj):
        item_object_list = models.Food.objects.filter(foodcategory = obj)
        ser = FoodSerializers(instance=item_object_list, many=True, context=self.context)
        image = []
        for item in  ser.data:
            image_dict = {}
            image_dict['id'] = item['id']
            image_dict['image'] = item['food_image']
            image.append(image_dict)
        return image

class FoodCategoryDetailSerializers(serializers.ModelSerializer):
    food = serializers.SerializerMethodField()
    # category = serializers.SerializerMethodField()

    class Meta:
        model =  models.FoodCategory
        fields = ['id','name','food']
    def get_food(self, obj):
        item_object_list = models.Food.objects.filter(foodcategory = obj)
        ser = FoodSerializers(instance=item_object_list, many=True, context=self.context)
        return ser.data
        # return [model_to_dict(row,fields=['id','name','price']) for row in item_object_list ]

    # def get_category(self, obj):
    #     object_list = models.FoodCategory.objects.all()
    #     return [model_to_dict(row,fields=['id','name']) for row in object_list ]



class FoodSerializers(serializers.ModelSerializer):
    class Meta:
        model =  models.Food
        fields = "__all__"


class FoodCommentSerializers(serializers.ModelSerializer):
    comment_type = serializers.CharField(source='get_comment_type_display')
    user = serializers.SerializerMethodField()
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model =  models.FoodComment
        fields = "__all__"

    def get_user(self, obj):
        detail_queryset = models.UserInfo.objects.filter(id=obj.user.id)
        # ser = UserInfoSerializers(instance=detail_queryset, many=True, context=self.context)
        # return ser.data
        return [model_to_dict(row,fields=['id','nickname','avatar',]) for row in detail_queryset ]

class FoodImageDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.FoodDetailsImage
        fields = "__all__"

class FoodInfoSerializers(serializers.ModelSerializer):
    food_image_list = serializers.SerializerMethodField()
    foodcomment = serializers.SerializerMethodField()
    shoop_cart_num = serializers.SerializerMethodField()

    class Meta:
        model = models.Food
        fields = "__all__"


    def get_foodcomment(self, obj):
        if not obj.foodcomment:
            return
        detail_queryset = models.FoodComment.objects.filter(food=obj)
        ser = FoodCommentSerializers(instance=detail_queryset, many=True, context=self.context)
        return ser.data

    def get_food_image_list(self, obj):
        detail_queryset = models.FoodDetailsImage.objects.filter(food=obj)
        ser = FoodImageDetailSerializers(instance=detail_queryset, many=True, context=self.context)
        return ser.data

    def get_shoop_cart_num(self, obj):
        token = self.context['request'].META.get('HTTP_AUTHORIZATION', None)
        user_object = models.UserInfo.objects.filter(token=token).first()
        # queryse = ShoppingCart.objects.filter(user = user_object).count()
        detail_queryset = ShoppingCart.objects.filter(user = user_object).count()
        if detail_queryset:
            # user_id = []
            # for row in detail_queryset:
            #     user_id.append( row.user.id)
            # # /print(user_id[0])
            # queryse = ShoppingCart.objects.filter(user = user_id[0]).count()
            # if queryse:
                # print(queryse)
                return [{"nums":detail_queryset}]
            # return [model_to_dict(row,fields=['nums']) for row in detail_queryset ]
        return [{"nums":0}]
class FoodSearchSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=True,max_length=30)
    foodcategory = serializers.CharField()
    price = serializers.IntegerField()
    status = serializers.IntegerField()
    food_image = serializers.ImageField()

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     return models.Food.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.name = validated_data.get('name', instance.name)
        # instance.goods_sn = validated_data.get('goods_sn', instance.goods_sn)
        # instance.sold_num = validated_data.get('sold_num', instance.sold_num)
        # instance.market_price = validated_data.get('market_price', instance.market_price)
        # instance.save()
        # return instance
class FoodCategorySerializers(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model =  models.FoodComment
        exclude = ['user','food']