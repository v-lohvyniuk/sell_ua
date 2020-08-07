from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name='home'),
    path("advert/<int:pk>/", views.AdvertDetailsView.as_view()),
    path("advert/<int:pk>/payment-delivery", views.PaymentDeliveryView.as_view(), name='checkout'),
    path("advert/<int:pk>/payment-delivery/submit", views.payment_delivery_submit, name='checkout-submit'),
    path("category/<slug:url>/", views.CategoryAdvertListView.as_view(), name='category'),
    path("orders/", views.OrderHistoryView.as_view(), name='order-history'),
]