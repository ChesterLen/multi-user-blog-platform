from django.views import generic as views
from django.urls import reverse_lazy
from multi_user_blog_platform.app_auth import forms


class UserRegistrationView(views.CreateView):
    form_class = forms.UserRegistrationForm
    template_name = 'user/registration.html'
    success_url = reverse_lazy('registration')