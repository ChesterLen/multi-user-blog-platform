from django.views import generic as views


class HomePageView(views.TemplateView):
    template_name = 'home/home_page.html'