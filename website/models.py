from django.db import models
from django.urls import reverse


class Category(models.Model):

    name = models.CharField("Назва", max_length=50)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    url = models.SlugField(max_length=50, default='root')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def get_url(self):
        return reverse("category", args=[self.url])


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


class AdvertStatusManager(models.Manager):

    def get_by_label(self, label):
        return self.get(label=label)


class AdvertStatus(models.Model):

    objects = AdvertStatusManager()
    label = models.CharField(max_length=25)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статуси"


class Advert(models.Model):

    title = models.CharField("Заголовок", max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Власник")
    date_published = models.DateTimeField("Дата публікації", auto_now=True)
    description = models.TextField("Опис", max_length=1000)
    price = models.DecimalField("Ціна", decimal_places=2, max_digits=10)
    is_price_final = models.BooleanField(default=False)
    status = models.ForeignKey(verbose_name="Статус", to=AdvertStatus, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    views = models.PositiveIntegerField("Перегляди", default=0)
    address = models.ForeignKey(verbose_name="Адреса відправлювача", to=UserAddress, on_delete=models.SET_NULL, null=True, blank=True)

    def get_cover_photo(self):
        all_images = self.advertphoto_set.all()
        if all_images:
            if self.advertphoto_set.filter(is_cover_photo=True):
                return self.advertphoto_set.filter(is_cover_photo=True).get().image.url
            else:
                return self.advertphoto_set.first().image.url
        return ''

    def get_advert_address(self):
        if self.address:
            return self.address
        else:
            return self.owner.useraddress_set.first()

    def is_advert_active(self):
        return self.status is not None \
               and self.status.label == "ADVERT_ACTIVE"

    def set_reserved(self):
        self.status = AdvertStatus.objects.get_by_label("ADVERT_RESERVED")
        self.save()

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


class DeliveryType(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип доставки"
        verbose_name_plural = "Типи доставки"

    @staticmethod
    def for_name(name):
        return DeliveryType.objects.get(name=name)


class ContactInfo(models.Model):

    email = models.EmailField()
    phone = models.CharField("Телефон", max_length=15)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Контактна інформація"
        verbose_name_plural = "Контактна інформація"


class OrderStatusManager(models.Manager):

    def get_by_label(self, label):
        return self.get(label=label)


class OrderStatus(models.Model):

    label = models.CharField(max_length=25)
    objects = OrderStatusManager()

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статуси"


class Order(models.Model):

    buyer = models.ForeignKey(verbose_name="Покупець", to=User, null=True, blank=True, on_delete=models.SET_NULL, related_name="buyer")
    owner = models.ForeignKey(verbose_name="Продавець", to=User, null=True, blank=True, on_delete=models.SET_NULL, related_name="seller")
    is_anonymous_sale = models.BooleanField(default=True)
    status = models.ForeignKey(verbose_name="Статус", to=OrderStatus, on_delete=models.SET_NULL, null=True)
    delivery_type = models.ForeignKey(verbose_name="Тип доставки", null=True, to=DeliveryType, on_delete=models.SET_NULL)
    delivery_address = models.ForeignKey(verbose_name="Адреса доставки", on_delete=models.SET_NULL, to=UserAddress, null=True, blank=True)
    contact_info = models.ForeignKey(verbose_name="Контактна інформація", on_delete=models.SET_NULL, to=ContactInfo, null=True)
    advert = models.ForeignKey(verbose_name="Оголошення", to=Advert, on_delete=models.SET_NULL, null=True)

    def get_seller(self):
        return self.advert.owner.get()

    def set_status_created(self):
        self.status = OrderStatus.objects.get_by_label("ORDER_CREATED")
        self.save()

    def set_delivery(self, delivery_type, address):
        self.delivery_type = delivery_type
        self.delivery_address = address
        self.save()

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"