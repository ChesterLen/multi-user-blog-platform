from django.urls import path
from multi_user_blog_platform.app_auth import views


urlpatterns = [
    path('', views.UserRegistrationView.as_view(), name='registration'),
    path('activate/account/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]