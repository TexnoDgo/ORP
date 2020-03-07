from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Order(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)  # Автор заказа. Автоматически
    date_create = models.DateTimeField(default=timezone.now)  # Время создания заказа. Автоматически
    title = models.CharField(max_length=100)  # Заголовок заказа
    description = models.TextField()  # Описание заказа
    amount = models.PositiveIntegerField()  # Кол-во изделий
    city = models.CharField(max_length=30)  # Грод заказа
    lead_time = models.DateField()  # Срок выполнения заказа
    proposed_budget = models.CharField(max_length=40)  # Предложеный бюджет
    activity = models.BooleanField()  # Активность заказа
    status = models.CharField(max_length=10)  # Статус заказ

    def __str__(self):
        return self.title
