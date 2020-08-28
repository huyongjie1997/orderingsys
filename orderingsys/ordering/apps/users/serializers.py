from rest_framework import serializers
import re
from users import models
from rest_framework.exceptions import ValidationError
from django_redis import get_redis_connection

def phone_validator(value):
    if not re.match(r"^(1[3|4|5|6|7|8|9])\d{9}$",value):
        raise ValidationError('手机格式错误')

class MessageSerializer(serializers.Serializer):
    phone = serializers.CharField(label='手机号',validators=[phone_validator,])

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(label='手机号', validators=[phone_validator, ])
    code = serializers.CharField(label='短信验证码',required=True, write_only=True, max_length=4, min_length=4,
                                 error_messages={
                                        "blank": "请输入验证码",
                                        "required": "请输入验证码",
                                        "max_length": "验证码格式错误",
                                        "min_length": "验证码格式错误"
                                 },help_text="验证码")
    nickname = serializers.CharField(label='昵称')
    avatar = serializers.CharField(label='头像')

    def validate_code(self, value):
        if len(value) !=4:
            raise ValidationError('短信格式错误')
        if not value.isdecimal():
            raise ValidationError('短信格式错误')

        phone = self.initial_data.get('phone')
        conn = get_redis_connection()
        code = conn.get(phone)
        if not code:
            raise ValidationError('验证码过期')
        if value != code.decode('utf-8'):
            raise ValidationError('验证码错误')
        return value
class UserInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model =  models.UserInfo
        fields = "__all__"

class AddressSerializers(serializers.ModelSerializer):
    singer_mobile = serializers.CharField(label='手机号', validators=[phone_validator, ])
    class Meta:
        model =  models.Address
        exclude = ['user','add_time']

class AddressDefaultSerializers(serializers.ModelSerializer):
    class Meta:
        model =  models.Address
        fields = "__all__"
