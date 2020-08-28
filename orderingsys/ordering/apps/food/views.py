from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView,RetrieveAPIView
from django.db.models import Q

from food import models
from food.serializers import IndexSerializers,FoodInfoSerializers,FoodCategoryDetailSerializers,FoodSearchSerializers,FoodCategorySerializers,FoodSerializers,CommentSerializers
from trade.models import OrderFoods,OrderInfo



###########获取分类数据列表#############
class IndexViews( ListAPIView):
    queryset = models.FoodCategory.objects.filter()
    serializer_class = IndexSerializers

class FoodViews( APIView):
    def get(self, request,*args,**kwargs):
        id = request.query_params.get('pk')
        print(id)
        if id == "0":
            detail_queryset = models.Food.objects.all()
            serializer = FoodSerializers(detail_queryset, many=True,context={'request':request})
            return Response(serializer.data)
        else:
            queryset = models.FoodCategory.objects.filter(id = id)
            # serializer_class = FoodCategoryDetailSerializers
            serializer = FoodCategoryDetailSerializers(queryset, many=True,context={'request':request})
            return Response(serializer.data)

##########获取分类详情数据列表#############
class FoodCategoryDetailViews( RetrieveAPIView):
    queryset = models.FoodCategory.objects
    serializer_class = FoodCategoryDetailSerializers


#############获取单条数据详情，相当于有filter的限制筛选条件#############
class FoodInfoViews(RetrieveAPIView):
    queryset = models.Food.objects
    serializer_class = FoodInfoSerializers

#############搜索信息接口#############
class FoodSearchViews(APIView):
    def get(self, request,*args,**kwargs):
        search = request.query_params.get('mix_kw')
        detail_queryset = models.Food.objects.filter(name=search)
        if  detail_queryset:
            serializer = FoodSearchSerializers(detail_queryset, many=True,context={'request':request})
            return Response(serializer.data)
        return Response({"statu": False,"msg":"请填写正确的菜品名称"})

class FoodCategoryViews(APIView):
    def get(self, request,*args,**kwargs):
        detail_queryset = models.FoodCategory.objects.all()
        dict=[{
            'id':0,
            'name':'全部'
        }]
        serializer = FoodCategorySerializers(detail_queryset, many=True,context={'request':request})
        for i in serializer.data:
            c = {}
            c['id']=i['id']
            c['name']=i['name']
            dict.append(c)
        return Response(dict)

class FoodCommentViews(APIView):
     def post(self, request,*args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user_object = models.UserInfo.objects.filter(token=token).first()
        order_sn = request.data['order_sn']
        order = OrderInfo.objects.filter(order_sn = order_sn)
        food = OrderFoods.objects.filter(order__in = order)

        score = request.data['score']
        print(score)
        global comment_type
        if score== '10':
            comment_type = 'praise'
        elif score== '6':
            comment_type = 'mid-review'
        elif score== '0':
            comment_type = 'bad'
        ser = CommentSerializers(data=request.data)
        print(comment_type)
        if ser.is_valid():
            for row in food:
                ser = CommentSerializers(data=request.data)
                ser.is_valid()
                ser.save(user = user_object,food_id = row.food.id, comment_type = comment_type)
            return Response({'status':True,'msg':"评论成功"})
        return Response({'status':False,'msg':"评论失败"})