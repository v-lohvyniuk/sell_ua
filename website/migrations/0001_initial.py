# Generated by Django 3.1 on 2020-08-10 19:22

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('date_published', models.DateTimeField(auto_now=True, verbose_name='Дата публікації')),
                ('description', models.TextField(max_length=1000, verbose_name='Опис')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ціна')),
                ('is_price_final', models.BooleanField(default=False)),
                ('views', models.PositiveIntegerField(default=0, verbose_name='Перегляди')),
            ],
            options={
                'verbose_name': 'Оголошення',
                'verbose_name_plural': 'Оголошення',
            },
        ),
        migrations.CreateModel(
            name='AdvertStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статуси',
            },
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15, verbose_name='Телефон')),
            ],
            options={
                'verbose_name': 'Контактна інформація',
                'verbose_name_plural': 'Контактна інформація',
            },
        ),
        migrations.CreateModel(
            name='DeliveryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': 'Тип доставки',
                'verbose_name_plural': 'Типи доставки',
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статуси',
            },
        ),
        migrations.CreateModel(
            name='WebsiteUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('reg_date', models.DateField(auto_now=True, verbose_name='Дата реєстрації')),
                ('phone', models.CharField(max_length=13, verbose_name='Номер телефону')),
                ('is_show_phone', models.BooleanField(default=False, verbose_name='Показувати телефон')),
            ],
            options={
                'verbose_name': 'Користувач',
                'verbose_name_plural': 'Користувачі',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=50, verbose_name='Область')),
                ('city', models.CharField(max_length=50, verbose_name='Місто')),
                ('street', models.CharField(max_length=50, verbose_name='Вулиця')),
                ('building_number', models.CharField(max_length=10, verbose_name='Номер будинку')),
                ('apartments', models.CharField(max_length=5, verbose_name='Номер квартири')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.websiteuser', verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Адреса',
                'verbose_name_plural': 'Адреси',
            },
        ),
        migrations.CreateModel(
            name='SellerFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.PositiveSmallIntegerField(verbose_name='Оцінка (0-5)')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_for_feedback', to='website.websiteuser', verbose_name='Продавець')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.websiteuser', verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Відгук',
                'verbose_name_plural': 'Відгуки',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_anonymous_sale', models.BooleanField(default=True)),
                ('advert', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.advert', verbose_name='Оголошення')),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buyer', to='website.websiteuser', verbose_name='Покупець')),
                ('contact_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.contactinfo', verbose_name='Контактна інформація')),
                ('delivery_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.useraddress', verbose_name='Адреса доставки')),
                ('delivery_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.deliverytype', verbose_name='Тип доставки')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller', to='website.websiteuser', verbose_name='Продавець')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.orderstatus', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Замовлення',
                'verbose_name_plural': 'Замовлення',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Назва')),
                ('url', models.SlugField(default='root')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.category')),
            ],
            options={
                'verbose_name': 'Категорія',
                'verbose_name_plural': 'Категорії',
            },
        ),
        migrations.CreateModel(
            name='AdvertPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='images/default-no-image.img', upload_to='images/', verbose_name='Зображення')),
                ('is_cover_photo', models.BooleanField(default=False, verbose_name='Обкладинка')),
                ('advert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.advert', verbose_name='Оголошення')),
            ],
            options={
                'verbose_name': 'Фото оголошення',
                'verbose_name_plural': 'Фото оголошення',
            },
        ),
        migrations.AddField(
            model_name='advert',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.useraddress', verbose_name='Адреса відправлювача'),
        ),
        migrations.AddField(
            model_name='advert',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.category', verbose_name='Категорія'),
        ),
        migrations.AddField(
            model_name='advert',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.websiteuser', verbose_name='Власник'),
        ),
        migrations.AddField(
            model_name='advert',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.advertstatus', verbose_name='Статус'),
        ),
    ]
