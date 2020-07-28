from django.views.generic import ListView
from .models import Advert


class HomePageView(ListView):

    model = Advert
    template_name = "website/home.html"