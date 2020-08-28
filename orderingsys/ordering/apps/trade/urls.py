from django.urls import path
from trade.views import TradeInfoViews,TradeOrderViews,TradeOrderListViews
urlpatterns = [
    # path(r'^news/(?P<pk>\d+)/$', news.NewsDetailView.as_view()),
    path('info/', TradeInfoViews.as_view()),
    path('order/', TradeOrderViews.as_view()),
    path('order/list/', TradeOrderListViews.as_view()),
]