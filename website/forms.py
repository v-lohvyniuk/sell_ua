from django.forms import Form
from django import forms


class Widgets:
    TEXT_INPUT_WIDGET = forms.TextInput(attrs={"class": "form-control"})
    TEXT_INPUT_WIDGET_SMALL = forms.TextInput(attrs={"class": "form-control w-40"})


class DeliveryTypeForm(Form):
    DELIVERY_CHOICES = [
        ('self', "Самовивіз"),
        ('delivery-np', "Доставка \"Нова пошта\""),
        ('courier-np', "Кур'єр \"Нова пошта\""),
                        ]
    delivery_type = forms.ChoiceField(choices=DELIVERY_CHOICES, widget=forms.RadioSelect, label="", initial='self')


class DeliveryAddressForm(Form):

    name_surname = forms.CharField(max_length=50, label="Ім'я та прізвище", widget=Widgets.TEXT_INPUT_WIDGET, required=False)
    region = forms.CharField(max_length=50, label="Область", widget=Widgets.TEXT_INPUT_WIDGET, required=False)
    sub_region = forms.CharField(max_length=50, label="Район", widget=Widgets.TEXT_INPUT_WIDGET, required=False)
    city = forms.CharField(max_length=50, label="Місто", widget=Widgets.TEXT_INPUT_WIDGET, required=False)
    street = forms.CharField(max_length=50, label="Вулиця", widget=Widgets.TEXT_INPUT_WIDGET, required=False)
    building_no = forms.CharField(max_length=50, label="Номер будинку", widget=Widgets.TEXT_INPUT_WIDGET_SMALL, required=False)
    apartments = forms.CharField(max_length=50, label="Номер квартири", widget=Widgets.TEXT_INPUT_WIDGET_SMALL, required=False)
    wrh_no = forms.CharField(max_length=50, label="Номер відділення 'Нова Пошта'", widget=Widgets.TEXT_INPUT_WIDGET_SMALL, required=False)


class ContactInfoForm(Form):

    email = forms.EmailField(widget=Widgets.TEXT_INPUT_WIDGET)
    phone = forms.CharField(max_length=15, label="Телефон", widget=Widgets.TEXT_INPUT_WIDGET)