from rest_framework import serializers
from multi_user_blog_platform.app_auth import models


class PetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PetImage
        fields = '__all__'


class PetImageCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PhotoComment
        fields = ['comment']