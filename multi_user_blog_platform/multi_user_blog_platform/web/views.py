from django.views import generic as views
from multi_user_blog_platform.app_auth import models
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

UserModel = get_user_model()


class HomePageView(views.TemplateView):
    template_name = 'home/home_page.html'

    def get_template_names(self):
        if self.request.user.is_authenticated:
            self.template_name = 'home/wall.html'
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        liked_publications = []

        for like in models.Like.objects.all():
            if like.liker == self.request.pet:
                liked_publications.append(like.publication)

        try:
            featured_pets = models.Pet.objects.all()[:4]
            context['featured_pets'] = featured_pets
            context['pets'] = models.Pet.objects.all()
            context['publications'] = models.Publication.objects.all()
            context['liked_publications'] = liked_publications
        except models.Pet.DoesNotExist as error:
            print(error)

        return context


class DogCatView(views.View):
    template_name = 'pet/dog_or_cat.html'

    def get(self, request):
        pet = getattr(request.user, 'pet', None)

        pet_kind_dict = {
            'dog': 'dog',
            'cat': 'cat'
        }

        first_key = next(iter(request.GET), None)

        if first_key and first_key in pet_kind_dict and pet:
            pet.specie = pet_kind_dict[first_key]
            pet.save()
            return redirect('profile_edit', pk=pet.pk)

        return render(request, self.template_name)