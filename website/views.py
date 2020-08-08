from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .forms import DeliveryTypeForm, DeliveryAddressForm, ContactInfoForm
from .models import Advert, Category, Order, DeliveryType, ContactInfo, AdvertStatus, OrderStatus
from .services import PlaceOrderService, OrderService, CategoryService, AdvertService


class HeaderAwareListView(ListView):
    extra_context = {"category_root": Category.objects.get(url="root")}


class HeaderAwareDetailView(DetailView):
    extra_context = {"category_root": Category.objects.get(url="root")}


class HomePageView(HeaderAwareListView):
    model = Advert
    template_name = "website/home.html"


class AdvertDetailsView(HeaderAwareDetailView):
    model = Advert

    def get(self, request, *args, **kwargs):
        advert = self.get_object()
        advert.increase_view_counter()
        return super().get(request, args, kwargs)


class CategoryAdvertListView(HeaderAwareListView):
    model = Advert
    slug_field = "url"
    template_name = "website/category.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        # get default impl
        context_data = super(CategoryAdvertListView, self).get_context_data(object_list=None, kwargs=kwargs)
        # extend with category info
        context_data['category'] = Category.objects.get(url=self.kwargs["url"])
        return context_data

    def get_queryset(self):
        query_url = self.kwargs["url"]
        if "root" in query_url:
            return AdvertService.get_active_adverts()
        else:
            self_and_descendants = CategoryService.get_category_and_descendants(query_url)
            return AdvertService.get_active_adverts_for_categories(category_list=self_and_descendants)


class PaymentDeliveryView(DetailView):
    model = Advert
    template_name = 'website/payment-delivery.html'
    extra_context = {
        "delivery_type_form": DeliveryTypeForm(),
        "delivery_address_form": DeliveryAddressForm(),
        "contact_info_form": ContactInfoForm()
    }


def payment_delivery_submit(request, pk):
    if request.method == 'POST':
        delivery_type = DeliveryTypeForm(request.POST)
        contact_info = ContactInfoForm(request.POST)
        if delivery_type.data['delivery_type'] == 'self':
            delivery_type = DeliveryType.for_name('self')
            contact_info = \
            ContactInfo.objects.get_or_create(email=contact_info.data['email'], phone=contact_info.data['phone'])[0]
            advert = Advert.objects.get(pk=pk)
            order = PlaceOrderService(delivery_type, None, contact_info, advert).place_order()
            return redirect(to='order-confirmation', pk=order.pk)


class OrderConfirmationView(HeaderAwareDetailView):

    model = Order
    template_name = "website/order_confirmation.html"


class OrderHistoryView(HeaderAwareListView):

    model = Order
    template_name = "website/order_history.html"

    def get_queryset(self):
        return OrderService.get_all_orders()
