from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django_js_reverse.views import urls_js

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('multi_user_blog_platform.web.urls')),
    path('register/', include('multi_user_blog_platform.app_auth.urls')),
    path('jsreverse', urls_js, name='js_reverse'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)