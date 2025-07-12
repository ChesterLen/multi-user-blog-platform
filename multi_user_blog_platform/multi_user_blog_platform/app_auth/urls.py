from django.urls import path
from multi_user_blog_platform.app_auth import views


urlpatterns = [
    path('', views.UserRegistrationView.as_view(), name='registration'),
]