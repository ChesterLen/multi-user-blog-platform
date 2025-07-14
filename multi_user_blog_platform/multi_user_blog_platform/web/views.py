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
        pet = None

        if request.user:
            pet = UserModel.objects.get(email=request.user.email).pet
        
        pet_kind_dict = {
            'dog': 'dog', 'cat': 'cat'
            }
        
        if self.request.GET:
            first_key = next(iter(self.request.GET))
            specie = pet_kind_dict[first_key]
            pet.specie = specie
            pet.save()
            return redirect('home_page')
        
        return render(request, self.template_name)