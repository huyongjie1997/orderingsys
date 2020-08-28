from django.shortcuts import render
import uuid
import random
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import status

from django_redis import get_redis_connection
from users import models,serializers
from utils.auth import UserAuthentication

from django.forms import model_to_dict

# Create your views here.

class LoginViews(APIView):
    def post(self,request,*args,**kwargs):
        ser = serializers.LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"status": False, 'message':'验证码错误'})

        phone = ser.validated_data.get('phone')
        nickname = ser.validated_data.get('nickname')
        avatar = ser.validated_data.get('avatar')
        user_object, flag = models.UserInfo.objects.get_or_create(

            phone=phone,
            defaults={
                "nickname": nickname,
                'avatar': avatar}
        )
        user_object.token = str(uuid.uuid4())
        user_object.save()
        return Response({"status": True, "data": {"token": user_object.token, 'phone': phone}})
        # return Response(ser.data,status=status.HTTP_201_CREATED)
        # return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)

class MessageView(APIView):
    """
    发送短信接口
    """

    def get(self, request, *args, **kwargs):
        ser = serializers.MessageSerializer(data=request.query_params)
        if not ser.is_valid():
            return Response({'status': False, 'message': '手机格式错误'})
        phone = ser.validated_data.get('phone')
        random_code = random.randint(1000, 9999)

        # result = send_message(phone,random_code)
        # if not result:
        #     return Response({"status": False, 'message': '短信发送失败'})

        print(random_code)

        conn = get_redis_connection()
        conn.set(phone, random_code, ex=60)

        return Response({"status": True, 'message': '发送成功'})

class AddressView(APIView):
    authentication_classes = [UserAuthentication,]
    def post(self,request,*args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user_object = models.UserInfo.objects.filter(token=token).first()
        ser = serializers.AddressSerializers(data=request.data)
        if ser.is_valid():
            if  request.data['area_str']== "请选择":
                ser.save(user = user_object,area_id = None,area_str = None)
                return Response({"data":ser.data,"status": True, 'msg': '发送成功'})
            ser.save(user = user_object)
            return Response({"data":ser.data,"status": True, 'msg': '发送成功'})
        return Response({"data":ser.data,"status": False, 'msg': '信息填写有误，请认真填写'})

    def get(self,request,*args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user_object = models.UserInfo.objects.filter(token=token).first()
        id = request.query_params.get("id")
        if user_object:
            if not id:
                address = models.Address.objects.filter(user = user_object)
                serializer = serializers.AddressDefaultSerializers(address, many=True,context={'request':request})
                return Response(serializer.data)
            address = models.Address.objects.filter(user = user_object,id = id)
            serializer = serializers.AddressDefaultSerializers(address, many=True,context={'request':request})
            return Response(serializer.data)
        return Response({"statu": False})

    def put(self,request,*args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user_object = models.UserInfo.objects.filter(token=token).first()
        id = request.data.get("id")
        try:
            default = models.Address.objects.filter(user = user_object,is_default = 1).update(is_default = 0)
            is_default = models.Address.objects.filter(user = user_object,id = id,is_default = 0).update(is_default = 1)
        except:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if default & (is_default):
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class AddressDefaultView(APIView):
    def put(self,request,*args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        user_object = models.UserInfo.objects.filter(token=token).first()
        id = request.data.get("id")
        try:
            default = models.Address.objects.filter(user = user_object,is_default = 1).update(is_default = 0)
            is_default = models.Address.objects.filter(user = user_object,id = id,is_default = 0).update(is_default = 1)
        except:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if default & (is_default):
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
