from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePageView.as_view()),
    path("advert/<int:pk>/", views.AdvertDetailsView.as_view()),
    path("category/<slug:url>/", views.CategoryAdvertListView.as_view(), name='category')
]