from django.urls import path
from multi_user_blog_platform.web import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('dog/cat/', views.DogCatView.as_view(), name='dog_or_cat'),
]