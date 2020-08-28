from django.urls import path
from users.views import LoginViews,MessageView,AddressView,AddressDefaultView
urlpatterns = [
    # path(r'^news/(?P<pk>\d+)/$', news.NewsDetailView.as_view()),
    path('login/', LoginViews.as_view()),
    path('message/', MessageView.as_view()),
    path('address/', AddressView.as_view()),
    path('address/default/', AddressDefaultView.as_view()),
]