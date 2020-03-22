from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Order(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)  # Автор заказа. Автоматически
    date_create = models.DateTimeField(default=timezone.now)  # Время создания заказа. Автоматически
    title = models.CharField(max_length=100)  # Заголовок заказа
    description = models.TextField()  # Описание заказа
    #order_files = models.ManyToManyField('Files', blank=True, related_name='orders_file')  # Прикрипленные файлы
    amount = models.PositiveIntegerField()  # Кол-во изделий
    city = models.CharField(max_length=30)  # Грод заказа
    lead_time = models.DateField()  # Срок выполнения заказа
    proposed_budget = models.CharField(max_length=40)  # Предложеный бюджет
    activity = models.BooleanField()  # Активность заказа
    status = models.CharField(max_length=10)  # Статус заказ
    categories = models.ManyToManyField('OperationCategories', blank=True, related_name='orders')

    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})


class OperationCategories(models.Model):
    title = models.CharField(max_length=30)

    objects = models.Manager()

    def __str__(self):
        return self.title


class Suggestion(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    date_create = models.DateTimeField(default=timezone.now)
    offer_description = models.TextField()
    deadline = models.DateTimeField()
    offer_price = models.PositiveIntegerField()
    status = models.CharField(max_length=10, default='N0ne')
    selected_offer = models.BooleanField()

    def __str__(self):
        return self.offer_description


class Message(models.Model):
    suggestion = models.ForeignKey(Suggestion, on_delete=models.PROTECT)
    date_create = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    status = models.CharField(max_length=10)
