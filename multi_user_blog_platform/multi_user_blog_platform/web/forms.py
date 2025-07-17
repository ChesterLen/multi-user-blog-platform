from django import forms
from multi_user_blog_platform.web import models


class PublicationForm(forms.ModelForm):
    class Meta:
        model = models.Publication
        fields = ['image', 'title', 'text']