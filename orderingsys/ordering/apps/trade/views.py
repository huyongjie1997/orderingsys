from django.shortcuts import render
import time
import  json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView,RetrieveAPIView
from rest_framework import status
from django.db.models import F
from food import models
from users.models import Address
from trade.models import ShoppingCart,OrderFoods,OrderInfo
from trade.serializers import TradeInfoSerializer,ShopCartDetailSerializer,OrderSerializer,OrderInfoSerializer,TradeOrderListSerializer
from utils.auth import UserAuthentication
# Create your views here.
class TradeInfoViews(APIView):
    authentication_classes = [UserAuthentication,]
    def post(self,request,*args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user_object = models.UserInfo.objects.filter(token=token).first()
        ser = TradeInfoSerializer(data=request.data)
        if ser.is_valid():
            ser.save(user = user_object)
            return Response(ser.data,status=status.HTTP_201_CREATED)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,*args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user_object = models.UserInfo.objects.filter(token=token).first()
        shopcart_object = ShoppingCart.objects.filter(user = user_object)
        if shopcart_object:
            food = models.Food.objects.filter(name__in = [i.food.name for i in shopcart_object])
            serializer = ShopCartDetailSerializer(food, many=True,context={'request':request})
            return Response(serializer.data)
        return Response({"statu": False})

    def delete(self, request, *args, **kwargs):
        """
        单删
            接口: /book/(pk)/, 数据: 空
        群删
            接口: /book/, 数据: [pk1, pk2, ...]
        """
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user_object = models.UserInfo.objects.filter(token=token).first()
        food_id_list = request.data
        pks = food_id_list['food_id']
        try:
            rows = ShoppingCart.objects.filter(user=user_object, food_id__in=pks).delete()
        except:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if rows:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class TradeOrderViews(APIView):
    authentication_classes = [UserAuthentication,]
    def post(self,request,*args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user_object = models.UserInfo.objects.filter(token=token).first()
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=request.user.id,
                                                       ranstr=random_ins.randint(10, 99))
        ser = OrderSerializer(data=request.data)
        food_list = request.data["goods"]
        nums = [row['nums'] for row in food_list]
        if ser.is_valid():
            ser.save(user = user_object,order_sn = order_sn)
            order = OrderInfo.objects.filter(order_sn = order_sn)
            food= models.Food.objects.filter(id__in = [i["id"] for i in food_list])
            shop_carts = ShoppingCart.objects.filter(user=user_object, food__in=food)
            if not shop_carts:
                cart = ShoppingCart()
                cart.user = user_object
                cart.food = food.first()
                cart.nums = nums[0]
                cart.save()

            # print(shop_carts)
            for shop_cart in ShoppingCart.objects.filter(user=user_object, food__in=food):
                order_goods = OrderFoods()
                order_goods.food = shop_cart.food
                order_goods.food_num = shop_cart.nums
                order_goods.order_id = order[0].id
                order_goods.save()
                #清空购物车
                shop_cart.delete()
            return Response(ser.data,status=status.HTTP_201_CREATED)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,*args,**kwargs):
        food_lists = request.query_params.get("goods")
        food= models.Food.objects.filter(id__in = [item["id"] for item in json.loads(food_lists)])
        if food:
            serializer = OrderInfoSerializer(food, many=True,context={'request':request})
            return Response(serializer.data)
        return Response({"statu": False})

class TradeOrderListViews(APIView):
    authentication_classes = [UserAuthentication,]
    def get(self,request,*args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user_object = models.UserInfo.objects.filter(token=token).first()
        orderinfo_status =request.query_params.get("status")
        order = OrderInfo.objects.filter(user = user_object,orderinfo_status = orderinfo_status)
        if order:
            serializer = TradeOrderListSerializer(order, many=True,context={'request':request})
            return Response(serializer.data)
        return Response({"statu": False,"msg":"获取失败"})
    def post(self,request,*args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user_object = models.UserInfo.objects.filter(token=token).first()
        orderinfo =request.data["order_sn"]
        print(orderinfo)
        if orderinfo:
            try:
             order = OrderInfo.objects.filter(user = user_object,order_sn = orderinfo).delete()
            except:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            if order:
                return Response({"status":200})
            else:
                return Response({"status":400})
