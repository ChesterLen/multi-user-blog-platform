from django.views import generic as views
from django.urls import reverse_lazy, reverse
from multi_user_blog_platform.app_auth import forms, tasks, tokens, models
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import views as auth_views, get_user_model, logout, mixins
from django.shortcuts import redirect, render
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

        context['form'] = forms.PublicationForm

        publications = models.Publication.objects.filter(pet=self.object)
        context['publications'] = publications

        liked_publications = []

        for like in models.Like.objects.all():
            if like.liker == self.request.pet:
                liked_publications.append(like.publication)

        context['liked_publications'] = liked_publications
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = forms.PublicationForm(request.POST)

        if form.is_valid():
            publication = form.save(commit=False)
            publication.pet = self.object
            publication.save()
            return redirect('profile_details', self.object.pk)
        
        return render(request, self.template_name)



class ProfileUpdateView(mixins.LoginRequiredMixin, views.UpdateView):
    queryset = models.Pet.objects.all()
    form_class = forms.PetUpdateForm
    template_name = 'user/profile_edit.html'

    def get_success_url(self):
        return reverse('profile_details', args=[self.object.pk])
    
    def form_valid(self, form):
        pet = form.save()
        images = self.request.FILES.getlist('images')

        for image in images:
            models.PetImage.objects.create(pet=pet, image=image)
        return super().form_valid(form)
    

class Followers(views.DetailView):
    queryset = models.Pet.objects.all()
    template_name = 'user/followers_following.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'followers' in str(self.request.path):
            followers = models.Follow.objects.filter(followed_pet=self.object.pk)
            context['followers'] = [pet.follower_pet for pet in followers]
            
        elif 'following' in str(self.request.path):
            following = models.Follow.objects.filter(follower_pet=self.object.pk)
            context['following'] = [pet.followed_pet for pet in following]

        following_pets = models.Follow.objects.filter(follower_pet=self.object.pk)
        context['following_pets'] = [pet.followed_pet for pet in following_pets]

        return context
    

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


def like(request, pk):
    pub_pk = request.GET.get('pub_id')
    publication = models.Publication.objects.get(pk=pub_pk)

    pet = models.Publication.objects.get(pk=pk).pet

    try:
        like = models.Like.objects.filter(publication=publication, liker=request.pet)
    except models.Like.DoesNotExist as error:
        print(error)
    
    if not like:
        like = models.Like.objects.create(publication=publication, liker=request.pet)
    
    if 'profile' in request.path:
        return redirect('profile_details', pet.pk)
    
    return redirect('home_page')


def unlike(request, pk):
    pub_pk = request.GET.get('pub_id')
    publication = models.Publication.objects.get(pk=pk)
    pet = models.Publication.objects.get(pk=pub_pk).pet

    try:
        like = models.Like.objects.filter(publication=publication, liker=request.pet)
    except models.Like.DoesNotExist as error:
        print(error)

    if like:
        like.delete()

    if 'profile' in request.path:
        return redirect('profile_details', pet.pk)
    
    return redirect('home_page')


def comment(request, pk):
    comment = request.POST.get('comment')
    publication = models.Publication.objects.get(pk=pk)
    pet = request.pet

    form = forms.CommentForm

    if form.is_valid:
        models.Comment.objects.create(comment=comment, publication=publication, pet=pet)
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def comment_edit(request, pk):
    comment = models.Comment.objects.get(pk=pk)
    comment_edit_value = request.POST.get('comment_edit')

    form = forms.CommentEditForm

    if form.is_valid:
        comment.comment = comment_edit_value
        comment.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def comment_delete(request, pk):
    comment = models.Comment.objects.get(pk=pk)

    comment.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def reply(request, pk):
    reply = request.POST.get('reply')
    publication = models.Publication.objects.get(pk=request.POST.get('pub_pk'))
    comment_pk = request.POST.get('com_pk')
    comment = models.Comment.objects.get(pk=comment_pk)

    to_pet = None

    if request.POST.get('to_pet'):
        print(request.POST.get('to_pet'))
        to_pet = models.Reply.objects.get(pk=request.POST.get('to_pet')).from_pet
    else:
        to_pet = models.Comment.objects.get(pk=comment_pk).pet
    
    from_pet = request.pet
    
    form = forms.ReplyForm

    if form.is_valid:
        models.Reply.objects.create(reply=reply, publication=publication, comment=comment, from_pet=from_pet, to_pet=to_pet)
        return redirect(request.META.get('HTTP_REFERER', 'refirect_if_referer_not_found'))

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def edit_reply(request, pk):
    reply = models.Reply.objects.get(pk=pk)
    reply_input = request.POST.get('edit_input')
    print(reply_input)

    form = forms.ReplyEditForm

    if form.is_valid:
        reply.reply = reply_input
        reply.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def delete_reply(request, pk):
    reply = models.Reply.objects.get(pk=pk)
    reply.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))