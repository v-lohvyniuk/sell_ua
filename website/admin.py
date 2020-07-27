from django.contrib import admin
from .models import Advert, SellerFeedback, Category, UserAddress, AdvertPhoto, User

admin.site.register(Advert)
admin.site.register(AdvertPhoto)
admin.site.register(User)
admin.site.register(SellerFeedback)
admin.site.register(Category)
admin.site.register(UserAddress)

