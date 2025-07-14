from django.contrib.auth import forms as auth_forms, get_user_model

UserModel = get_user_model()


class UserRegistrationForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['email', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''