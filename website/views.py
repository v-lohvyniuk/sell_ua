from django.views.generic import ListView, DetailView
from .models import Advert, Category


class HeaderAwareListView(ListView):
    extra_context = {"category_root": Category.objects.get(url="root")}


class HeaderAwareDetailView(DetailView):
    extra_context = {"category_root": Category.objects.get(url="root")}


class HomePageView(HeaderAwareListView):

    model = Advert
    template_name = "website/home.html"


class AdvertDetailsView(HeaderAwareDetailView):

    model = Advert
    extra_context = {"category_root": Category.objects.get(url="root")}


class CategoryAdvertListView(HeaderAwareListView):

    model = Advert
    slug_field = "url"
    template_name = "website/category.html"

    def get_context_data(self, *, object_list=None,  **kwargs):
        # get standard context data
        context_data = super(CategoryAdvertListView, self).get_context_data(object_list=None, kwargs=kwargs)
        # populate category info
        context_data['category'] = Category.objects.get(url=self.kwargs["url"])
        return context_data

    def get_queryset(self):
        query_url = self.kwargs["url"]
        if "root" in  query_url:
            return Advert.objects.all()
        else:
            category = Category.objects.get(url=query_url)
            return Advert.objects.filter(category=category)
