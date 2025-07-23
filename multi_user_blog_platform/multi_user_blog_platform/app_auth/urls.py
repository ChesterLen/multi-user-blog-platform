from django.urls import path, include
from multi_user_blog_platform.app_auth import views


urlpatterns = [
    path('', views.UserRegistrationView.as_view(), name='registration'),
    path('activate/account/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', include([
        path('details/<int:pk>/', views.ProfileDetails.as_view(), name='profile_details'),
        path('update/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile_edit'),
        path('follow/<int:pk>/', views.follow, name='follow'),
        path('unfollow/<int:pk>/', views.unfollow, name='unfollow'),
        path('followers/<int:pk>/', views.Followers.as_view(), name='followers'),
        path('following/<int:pk>/', views.Followers.as_view(), name='following'),
        path('like/<int:pk>/', views.like, name='like'),
        path('unlike/<int:pk>/', views.unlike, name='unlike'),
        path('comment/<int:pk>/', views.comment, name='comment'),
        path('reply/<int:pk>/', views.reply, name='reply'),
        path('reply/reply/<int:pk>/', views.reply_reply, name='reply_reply'),
    ]))
]