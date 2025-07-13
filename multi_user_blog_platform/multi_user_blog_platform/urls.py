from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('multi_user_blog_platform.web.urls')),
    path('register/', include('multi_user_blog_platform.app_auth.urls')),
]
