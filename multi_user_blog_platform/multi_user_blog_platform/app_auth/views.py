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
        context['followers'] = self.object.followers.all().count()
        context['following'] = self.object.following.all().count()

        try:
            pet = models.Pet.objects.get(pk=self.object.pk)
            user_pet = models.Pet.objects.get(pk=self.request.user.pet.pk)

        except models.Pet.DoesNotExist as error:
            print(error)

        if pet and user_pet:
            following = models.Follow.objects.filter(followed=pet, follower=user_pet)
            context['following_pet'] = following

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
    try:
        pet = models.Pet.objects.get(pk=pk)
        user_pet = models.Pet.objects.get(pk=request.user.pet.pk)
    except models.Pet.DoesNotExist as error:
        print(error)

    if pet != user_pet:
        if not models.Follow.objects.filter(followed=pet, follower=user_pet).exists():
            models.Follow.objects.create(followed=pet, follower=user_pet)
        

    return redirect('profile_details', pk=pk)


def unfollow(request, pk):
    try:
        pet = models.Pet.objects.get(pk=pk)
        user_pet = models.Pet.objects.get(pk=request.user.pet.pk)
    except models.Pet.DoesNotExist as error:
        print(error)

    following = models.Follow.objects.filter(followed=pet, follower=user_pet)
    if following:
        following.delete()
    
    return redirect('profile_details', pk)


class FollowersFollowingView(mixins.LoginRequiredMixin, views.DetailView):
    login_url = reverse_lazy('login')
    queryset = models.Pet.objects.all()
    template_name = 'user/followers_following.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if 'followers' in str(self.request.path):
            followers = self.object.followers.all()
            context['followers'] = [models.Pet.objects.get(pk=pet.follower_id) for pet in followers]
            
            for pet in context['followers']:
                following_pet = models.Follow.objects.filter(followed=pet, follower=self.request.user.pet)
                if following_pet:
                    context['following_pet'] = following_pet


        elif 'following' in str(self.request.path):
            following = self.object.following.all()
            context['following'] = [models.Pet.objects.get(pk=pet.followed_id) for pet in following]

            for pet in context['following']:
                followed_by_pet = models.Follow.objects.filter(followed=self.request.user.pet, follower=pet)
                if followed_by_pet:
                    context['followed_by_pet'] = followed_by_pet

        return context