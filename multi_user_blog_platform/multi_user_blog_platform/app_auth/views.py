from django.views import generic as views
from django.urls import reverse_lazy, reverse
from multi_user_blog_platform.app_auth import forms, tasks, tokens, models
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import views as auth_views, get_user_model, logout
from django.shortcuts import redirect
from django.conf import settings


UserModel = get_user_model()


class UserRegistrationView(views.CreateView):
    form_class = forms.UserRegistrationForm
    template_name = 'user/registration.html'
    success_url = reverse_lazy('registration')

    def form_valid(self, form):
        user = form.save()
        user_email = form.cleaned_data['email']
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = tokens.account_activate_password_reset_token_generator.make_token(user=user)

        tasks.send_confirmation_email.delay(uid=uid, token=token, site_url=settings.SITE_URL, user_email=user_email)

        return super().form_valid(form)
    

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(force_str(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (ValueError, TypeError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and tokens.account_activate_password_reset_token_generator.check_token(user=user, token=token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('registration')
    

class LoginView(auth_views.LoginView):
    template_name = 'user/login.html'


class LogoutView(views.View):
    def get(self, request):
        logout(request)
        return redirect('registration')
    

class ProfileDetails(views.DetailView):
    queryset = models.Pet.objects.all()
    template_name = 'user/profile_details.html'


class ProfileUpdateView(views.UpdateView):
    queryset = models.Pet.objects.all()
    form_class = forms.PetUpdateForm
    template_name = 'user/profile_update.html'

    def get_success_url(self):
        return reverse('profile_details', args=[self.object.pk])