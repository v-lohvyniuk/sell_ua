from django.contrib.auth.forms import UserCreationForm
from django import forms

from website.models import WebsiteUser


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=254, help_text="Required valid email field")

    class Meta:
        model = WebsiteUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
