"""orderingsys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
import  xadmin
from django.urls import re_path
from django.views.static import serve
from orderingsys.settings import  MEDIA_ROOT
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#配置goods的url
# router.register(r'goods', GoodsListViewSet)
# 配置Category的url
# router.register(r'categorys', CategoryViewSet, base_name="categorys")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    #rest_framework
    path('api-auth/',include('rest_framework.urls')),
    #drf文档，title自定义
    path('docs',include_docs_urls(title='微信小程序订餐系统')),
    #富文本编辑器
    path('ueditor/',include('DjangoUeditor.urls' )),
    #文件
    path('media/<path:path>',serve,{'document_root':MEDIA_ROOT}),
    # token
    path('api-token-auth/', views.obtain_auth_token),
    # jwt的token认证接口
    path('login/', obtain_jwt_token ),
    #商品列表页
    # re_path('^', include(router.urls)),
    path('food/',include('food.urls' )),
    path('trade/',include('trade.urls' )),
    path('users/',include('users.urls' )),
]
