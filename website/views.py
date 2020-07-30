from django.views.generic import ListView, DetailView
from .models import Advert


class HomePageView(ListView):

    model = Advert
    template_name = "website/home.html"


class AdvertDetailsView(DetailView):
    model = Advert
