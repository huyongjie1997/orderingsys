import xadmin
from food.models import Food,FoodCategory,FoodDetailsImage,FoodComment
class FoodXadmin(object):
    #显示的列
    list_display = ['id','foodcategory', 'name', "comment_count","month_count","price","summary","food_image"]
    #可以搜索的字段
    search_fields = ['foodcategory', 'name', "price","summary" ]
    #列表页可以直接编辑的
    list_editable = [ 'name', "comment_count","month_count",]
    #过滤器
    list_filter = ['foodcategory', 'name', "price"]
    #富文本编辑器
    style_fields = {"summary": "ueditor"}



class FoodCategoryXadmin(object):
    #显示的列
    list_display = ['name', 'add_time']
    #可以搜索的字段
    search_fields = ['name']
    #列表页可以直接编辑的
    list_editable = [ 'name',]
    #过滤器
    list_filter = ['name']



class FoodDetailsImageXadmin(object):
    #显示的列
    list_display = ['food','food_detail_image', 'created_time']
    #可以搜索的字段
    search_fields = ['food']
    #列表页可以直接编辑的
    list_editable = [ 'food',]
    #过滤器
    list_filter = ['food',]

class FoodCommentXadmin(object):
    #显示的列
    list_display = ['food','user', 'comment','comment_type','created_time']
    #可以搜索的字段
    search_fields = ['food','user','comment_type']
    #列表页可以直接编辑的
    list_editable = [ 'food',]
    #过滤器
    list_filter = ['food',]

xadmin.site.register(FoodDetailsImage,FoodDetailsImageXadmin)
xadmin.site.register(Food, FoodXadmin)
xadmin.site.register(FoodCategory, FoodCategoryXadmin)
xadmin.site.register(FoodComment, FoodCommentXadmin)