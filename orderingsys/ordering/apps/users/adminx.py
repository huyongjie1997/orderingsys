import xadmin
from xadmin import views
from users.models import UserInfo,Address

#配置xadmin主题,注册的时候要用到专用的view去注册
class BaseXadminSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = '微信点餐后台系统'
    site_footer = '基于Django REST framework的微信点餐后台系统'
    #菜单栏折叠
    # menu_style = 'accordion'



class UserInfoXadmin(object):
    #显示的列
    list_display = ['phone', 'nickname', "avatar","token","revenue","balance"]
    #可以搜索的字段
    search_fields = ['nickname','phone' ]
    #列表页可以直接编辑的
    list_editable = ["revenue","balance" ,]
    #过滤器
    list_filter = ['phone', 'nickname', "avatar","token"]
    #富文本编辑器
    # style_fields = {"goods_desc": "ueditor"}


class AddressXadmin(object):
    #显示的列
    list_display = ['user', 'address', "province_str","city_str","area_str","signer_name","singer_mobile"]
    #可以搜索的字段
    search_fields = ['user', 'address', "province_str","city_str","area_str","signer_name","singer_mobile"]
    #列表页可以直接编辑的
    list_editable = ['user', 'address', "province_str","city_str","area_str","signer_name","singer_mobile"]
    #过滤器
    list_filter = ['user', 'address', "province_str","city_str","area_str","signer_name","singer_mobile"]


xadmin.site.register(UserInfo, UserInfoXadmin)
xadmin.site.register(Address, AddressXadmin)
#注册主题类
xadmin.site.register(views.BaseAdminView,BaseXadminSetting)
#注册全局样式的类
xadmin.site.register(views.CommAdminView,GlobalSettings)