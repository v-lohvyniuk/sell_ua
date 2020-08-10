from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from .models import Advert, SellerFeedback, Category, UserAddress, AdvertPhoto, WebsiteUser, Order, DeliveryType


class UserAddressAdmin(ModelAdmin):
    list_display = ['owner', 'city', 'street', 'building_number']


class OrderAdmin(ModelAdmin):
    list_display = ['status', 'advert']


class DeliveryTypeAdmin(ModelAdmin):
    list_display = ['name']


class AddressInline(TabularInline):
    model = UserAddress
    extra = 1


class AdvertPhotoInline(TabularInline):
    model = AdvertPhoto
    extra = 1


class AdvertAdmin(ModelAdmin):
    fieldsets = [
        ("Загальне", {"fields": ['title', 'owner', 'price', 'category', 'description', 'address']}),
        ("Адміністрування", {"fields": ['is_price_final', 'status']}),
    ]
    inlines = [AdvertPhotoInline]


class UserAdmin(ModelAdmin):
    inlines = [AddressInline]


admin.site.register(Advert, AdvertAdmin)
admin.site.register(WebsiteUser, UserAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
admin.site.register(SellerFeedback)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(DeliveryType, DeliveryTypeAdmin)


