from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .forms import DeliveryTypeForm, DeliveryAddressForm, ContactInfoForm
from .models import Advert, Category, Order, DeliveryType, ContactInfo, AdvertStatus, OrderStatus


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

    def get(self, request, *args, **kwargs):
        advert = self.get_object()
        Advert.objects.filter(pk=advert.pk).update(views=advert.views + 1)
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
            return Advert.objects.all()
        else:
            category = Category.objects.get(url=query_url)
            self_and_descendants = self.get_all_descendants(category, set())
            self_and_descendants.add(category)
            return Advert.objects.filter(category__in=self_and_descendants)

    def get_all_descendants(self, category, result_set):
        for category in category.category_set.all():
            result_set.add(category)
            self.get_all_descendants(category, result_set)
        return result_set


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
        # delivery_Address = DeliveryAddressForm(request.POST)
        contact_info = ContactInfoForm(request.POST)
        order = Order()
        if delivery_type.data['delivery_type'] == 'self':
            order.delivery_type = DeliveryType.for_name('self')
            order.is_anonymous_sale = True
            order.contact_info = ContactInfo.objects.get_or_create(email=contact_info.data['email'], phone=contact_info.data['phone'])[0]
            order.advert = Advert.objects.get(pk=pk)
            order.advert.status = AdvertStatus.objects.get(label="ADVERT_RESERVED")
            order.advert.save()
            order.status = OrderStatus.objects.get(label="ORDER_CREATED")
            order.save()
    return redirect(to='home')


