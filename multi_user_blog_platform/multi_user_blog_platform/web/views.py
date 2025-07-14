from django.views import generic as views
from multi_user_blog_platform.app_auth import models
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

UserModel = get_user_model()


class HomePageView(views.TemplateView):
    template_name = 'home/home_page.html'


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
            return redirect('profile_update', pk=pet.pk)

        return render(request, self.template_name)