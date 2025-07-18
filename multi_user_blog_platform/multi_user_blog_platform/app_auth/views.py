from django.views import generic as views
from django.urls import reverse_lazy, reverse
from multi_user_blog_platform.app_auth import forms, tasks, tokens, models
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import views as auth_views, get_user_model, logout, mixins
from django.shortcuts import redirect
from django.conf import settings


UserModel = get_user_model()


class UserRegistrationView(views.CreateView):
    form_class = forms.UserRegistrationForm
    template_name = 'user/registration.html'
    success_url = reverse_lazy('registration')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile_details', request.user.pet.pk)
        return super().dispatch(request, *args, **kwargs)

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


class LogoutView(mixins.LoginRequiredMixin, views.View):
    login_url = reverse_lazy('login')
    def get(self, request):
        logout(request)
        return redirect('home_page')
    

class ProfileDetails(mixins.LoginRequiredMixin, views.DetailView):
    login_url = reverse_lazy('login')
    queryset = models.Pet.objects.all()
    template_name = 'user/profile_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        following = models.Follow.objects.filter(followed_pet=self.object.pk, follower_pet=self.request.user.pet.pk)
        context['following'] = following

        followers = models.Follow.objects.filter(followed_pet=self.object.pk)
        context['followers'] = len(followers)

        following_pets = models.Follow.objects.filter(follower_pet=self.object.pk)
        context['following_pets'] = len(following_pets)

        return context


class ProfileUpdateView(mixins.LoginRequiredMixin, views.UpdateView):
    queryset = models.Pet.objects.all()
    form_class = forms.PetUpdateForm
    template_name = 'user/profile_update.html'

    def get_success_url(self):
        return reverse('profile_details', args=[self.object.pk])
    
    def form_valid(self, form):
        pet = form.save()
        images = self.request.FILES.getlist('images')

        for image in images:
            models.PetImage.objects.create(pet=pet, image=image)
        return super().form_valid(form)
    

def follow(request, pk):
    pet_to_follow = models.Pet.objects.get(pk=pk)
    pet_follower = models.Pet.objects.get(pk=request.user.pet.pk)

    models.Follow.objects.create(followed_pet=pet_to_follow, follower_pet=pet_follower)

    next_url = request.GET.get('next')

    if next_url:
        return redirect(next_url)
    
    return redirect('profile_details', pk)


def unfollow(request, pk):
    pet_to_unfollow = models.Pet.objects.get(pk=pk)
    pet_unfollower = models.Pet.objects.get(pk=request.user.pet.pk)

    unfollow = models.Follow.objects.filter(followed_pet=pet_to_unfollow, follower_pet=pet_unfollower).first()

    if unfollow:
        unfollow.delete()

    next_url = request.GET.get('next')

    if next_url:
        return redirect(next_url)

    return redirect('profile_details', pk)


class Followers(views.DetailView):
    queryset = models.Pet.objects.all()
    template_name = 'user/followers_following.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'followers' in str(self.request.path):
            followers = models.Follow.objects.filter(followed_pet=self.object.pk)
            context['followers'] = [pet.follower_pet for pet in followers]
            
        elif 'following' in str(self.request.path):
            followers = models.Follow.objects.filter(followed_pet=self.object.pk)
            context['followers'] = [pet.follower_pet for pet in followers]
            following = models.Follow.objects.filter(follower_pet=self.object.pk)
            context['following'] = [pet.followed_pet for pet in following]

        following_pets = models.Follow.objects.filter(follower_pet=self.object.pk)
        context['following_pets'] = [pet.followed_pet for pet in following_pets]

        return context