from django.urls import path, include
from multi_user_blog_platform.app_auth import views


urlpatterns = [
    path('', views.UserRegistrationView.as_view(), name='registration'),
    path('activate/account/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', include([
        path('details/<int:pk>/', views.ProfileDetails.as_view(), name='profile_details'),
        path('update/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile_update'),
        path('follow/<int:pk>/', views.follow, name='follow'),
        path('unfollow/<int:pk>/', views.unfollow, name='unfollow'),
        path('followers/<int:pk>/', views.FollowersFollowingView.as_view(), name='followers'),
        path('following/<int:pk>/', views.FollowersFollowingView.as_view(), name='following'),
    ]))
]