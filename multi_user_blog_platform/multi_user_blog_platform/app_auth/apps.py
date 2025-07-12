from django.apps import AppConfig


class AppAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'multi_user_blog_platform.app_auth'

    def ready(self):
        import multi_user_blog_platform.app_auth.signals