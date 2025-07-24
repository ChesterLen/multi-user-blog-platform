from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms
from multi_user_blog_platform.app_auth import models

UserModel = get_user_model()


class UserRegistrationForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['email', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['password2'].label = 'Repeat password'


class PetUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Pet
        fields = ['name', 'description', 'age', 'breed']


class PublicationForm(forms.ModelForm):
    class Meta:
        model = models.Publication
        fields = ['title', 'text']


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['comment']


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['comment']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = models.Reply
        fields = ['reply']