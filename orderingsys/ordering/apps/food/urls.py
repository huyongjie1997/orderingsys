from django.urls import path
from food.views import IndexViews,FoodInfoViews,FoodCategoryDetailViews,FoodSearchViews,FoodCategoryViews,FoodViews,FoodCommentViews
urlpatterns = [
    # path(r'^news/(?P<pk>\d+)/$', news.NewsDetailView.as_view()),
    path('index/', IndexViews.as_view()),
    path('category/', FoodCategoryViews.as_view()),
    path('category/<int:pk>/', FoodCategoryDetailViews.as_view()),
    path('food/', FoodViews.as_view()),
    path('search/', FoodSearchViews.as_view()),
    path('info/<int:pk>/', FoodInfoViews.as_view()),
    path('comment/', FoodCommentViews.as_view()),
]