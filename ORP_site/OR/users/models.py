from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from orders.models import Suggestion, OperationCategories
from django.conf import settings


class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    def __unicode__(self):
        return str(self.stripe_id)


class Profile(models.Model):
    TIMING_CHOICE = (
        ('Никогда', '0 часов'),
        ('Каждый час', '1 час'),
        ('Каждые 3 часа', '3 часа'),
        ('Каждые 6 часов', '6 часов'),
        ('Каждые 12 часов', '12 часов'),
        ('Каждые 24 часа', '24 часа'),
    )

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    rating = models.PositiveIntegerField(default=0)

    # ----------------------------------------Уведомления------------------------------------------------
    # Получать уведомления о новых заказа в категории?
    notifications = models.BooleanField(default=False, verbose_name='Получать уведомления?')
    # Получать уведомления в личный аккаунт
    notifi_account = models.BooleanField(default=False, verbose_name='Уведомления в кабинет?')
    # Получать уведомления на эл. почту
    notifi_email = models.BooleanField(default=False, verbose_name='Уведомления на почту?')
    # Поулчать уведомления по смс
    notifi_sms = models.BooleanField(default=False, verbose_name='Уведомления по СМС')
    # Получать уведомлекния новостях сайта
    notifi_news = models.BooleanField(default=False, verbose_name='Новости?')
    # Получать уведомления о Статьях на сайте
    notifi_articles = models.BooleanField(default=False, verbose_name='Статьи?')
    # Получать уведомления об обновлениях сайта.
    notifi_updates = models.BooleanField(default=False, verbose_name='Обновления?')
    # Частота обновления
    timing = models.CharField(max_length=30, choices=TIMING_CHOICE, default='Никогда', verbose_name='')
    # Категории уведомления
    categories = models.ManyToManyField(OperationCategories, blank=True, related_name='profile',
                                        verbose_name='Категории для уведомлений')
    # -------------------------------------------Уведомления----------------------------------------------

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):  # Преобразование изображения
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class CompanyProfile(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.TextField(verbose_name='Сокращенное название компании', default='CompanyName')
    edrpou = models.CharField(max_length=10, verbose_name='ЕДРПОУ')
    officialName = models.TextField(verbose_name='Официальное название компании', default='OfficialCompanyName')
    address = models.TextField(verbose_name='Адрес регистрации компании', default='CompanyAddress')
    mainPerson = models.CharField(max_length=255, verbose_name='Руководитель организации', default='CompanyMainPerson')
    occupation = models.TextField(verbose_name='Основной вид деятельности организации', default='CompanyOccupation')
    status = models.CharField(max_length=255, verbose_name='Состояние организации', default='CompanyStatus')

    def __str__(self):
        return self.name
