from django.views.generic import ListView, DetailView
from .models import Advert, Category


class HomePageView(ListView):

    model = Advert
    template_name = "website/home.html"
    extra_context = {"category_root": Category.objects.get(name="Всі категорії")}


class AdvertDetailsView(DetailView):

    model = Advert
    extra_context = {"category_root": Category.objects.get(name="Всі категорії")}
