import xadmin
from trade.models import ShoppingCart,OrderInfo,OrderFoods
class ShoppingCartAdmin(object):
    list_display = ["user", "food", "nums", ]


class OrderInfoAdmin(object):
    list_display = ["user", "order_sn",  "trade_no", "pay_status", "post_script", "order_mount",
                    "order_mount", "pay_time", "add_time"]

    class OrderFoodInline(object):
        model = OrderFoods
        exclude = ['add_time', ]
        extra = 1
        style = 'tab'

    inlines = [OrderFoodInline, ]


xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)