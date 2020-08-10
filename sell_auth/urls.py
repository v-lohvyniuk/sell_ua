from django.urls import path, include

from . import views
urlpatterns = [
    path('register/', views.registerPage, name="register"),
]
#
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
