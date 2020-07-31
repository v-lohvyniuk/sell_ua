import os

from django.db import models


class Category(models.Model):

    name = models.CharField("Назва", max_length=50)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class User(models.Model):

    first_name = models.CharField("Ім'я", max_length=50)
    last_name = models.CharField("Прізвище", max_length=50)
    reg_date = models.DateField("Дата реєстрації", auto_now=True)
    phone = models.CharField("Номер телефону", max_length=13)
    is_show_phone = models.BooleanField("Показувати телефон", default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"


class UserAddress(models.Model):

    owner = models.ForeignKey(verbose_name="Користувач", to=User, on_delete=models.CASCADE)
    region = models.CharField("Область", max_length=50)
    city = models.CharField("Місто", max_length=50)
    street = models.CharField("Вулиця", max_length=50)
    building_number = models.CharField("Номер будинку", max_length=10)
    apartments = models.CharField("Номер квартири", max_length=5)

    class Meta:
        verbose_name = "Адреса"
        verbose_name_plural = "Адреси"


class Advert(models.Model):

    title = models.CharField("Заголовок", max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Власник")
    date_published = models.DateField("Дата публікації", auto_now=True)
    description = models.TextField("Опис", max_length=1000)
    price = models.DecimalField("Ціна", decimal_places=2, max_digits=10)
    is_price_final = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)
    is_reviewed = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    views = models.PositiveIntegerField("Перегляди", default=0)
    address = models.ForeignKey(verbose_name="Адреса відправлювача", to=UserAddress, on_delete=models.SET_NULL, null=True, blank=True)

    def get_cover_photo(self):
        all = self.advertphoto_set.all()
        if all:
            if self.advertphoto_set.filter(is_cover_photo=True):
                return self.advertphoto_set.filter(is_cover_photo=True).get().image.url
            else:
                return self.advertphoto_set.first().image.url
        return ''

    def __str__(self):
        return f"{self.title} -  {self.owner} - {self.price}"

    class Meta:
        verbose_name = "Оголошення"
        verbose_name_plural = "Оголошення"


class AdvertPhoto(models.Model):

    advert = models.ForeignKey(Advert, verbose_name="Оголошення", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", verbose_name="Зображення", default='images/default-no-image.img')
    url = models.SlugField
    is_cover_photo = models.BooleanField("Обкладинка", default=False)

    class Meta:
        verbose_name = "Фото оголошення"
        verbose_name_plural = "Фото оголошення"


class SellerFeedback(models.Model):

    seller = models.ForeignKey(verbose_name="Продавець", to=User, on_delete=models.CASCADE, related_name="seller_for_feedback")
    user = models.ForeignKey(verbose_name="Користувач", to=User, on_delete=models.SET_NULL, null=True)
    mark = models.PositiveSmallIntegerField("Оцінка (0-5)")

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
