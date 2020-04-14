from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from orders.models import Suggestion


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    rating = models.PositiveIntegerField(default=0)

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
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.TextField(verbose_name='Сокращенное название компании')
    edrpou = models.CharField(max_length=10, verbose_name='ЕДРПОУ')
    officialName = models.TextField(verbose_name='Официальное название компании')
    address = models.TextField(verbose_name='Адрес регистрации компании')
    mainPerson = models.CharField(verbose_name='Руководитель организации')
    occupation = models.TextField(verbose_name='Основной вид деятельности организации')
    status = models.CharField(verbose_name='Состояние организации')

    def __str__(self):
        return self.name
