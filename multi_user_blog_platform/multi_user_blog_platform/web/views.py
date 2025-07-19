from django.views import generic as views
from multi_user_blog_platform.app_auth import models
from multi_user_blog_platform.web import forms
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

UserModel = get_user_model()


class HomePageView(views.TemplateView):
    template_name = 'home/home_page.html'

    def get_template_names(self):
        if self.request.user.is_authenticated:
            self.template_name = 'home/wall.html'
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            featured_pets = models.Pet.objects.all()[:4]
            context['featured_pets'] = featured_pets
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
            return redirect('profile_update', pk=pet.pk)

        return render(request, self.template_name)
    

class PublicationView(views.CreateView):
    template_name = 'user/profile_details.html'
    form_class = forms.PublicationForm
    
    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.request.user.pet.pk})
    
    def form_valid(self, form):
        publication = form.save(commit=False)
        publication.pet = self.request.pet
        publication = form.save(commit=True)
        return super().form_valid(form)