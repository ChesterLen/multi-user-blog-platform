from django.db import models
from multi_user_blog_platform.app_auth import models as app_auth_models

class Publication(models.Model):
    image = models.ImageField(upload_to='publication_images', null=True, blank=True)
    title = models.CharField(max_length=300, null=False, blank=False)
    text = models.TextField(max_length=1500, null=False, blank=False)

    pet = models.ForeignKey(to=app_auth_models.Pet, on_delete=models.CASCADE)