from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class AllCity(models.Model):
    title = models.CharField(max_length=50, default='not_selected')

    objects = models.Manager()

    def __str__(self):
        return self.title


class Order(models.Model):
    BUDGET_EXAMPLE = (
        ('Неизвестный', 'Неизвестный'),
        ('Малый 20-50$', 'Малый 20-50$'),
        ('Средний 50-250$', 'Средний 50-250$'),
        ('Высокий 250$+', 'Высокий 250$+')
    )

    ORDER_STATUS = (
        ('В обсуждении', 'В обсуждении'),
        ('В работe', 'В работe'),
        ('Выполненый', 'Выполненый'),
        ('Отменённый', 'Отменённый'),
    )

    author = models.ForeignKey(User, on_delete=models.PROTECT)  # Автор заказа. Автоматически
    date_create = models.DateTimeField(default=timezone.now)  # Время создания заказа. Автоматически
    title = models.CharField(max_length=100, verbose_name='Заголовок')  # Заголовок заказа
    description = models.TextField(verbose_name='Описание заказ')  # Описание заказа
    #order_files = models.ManyToManyField('Files', blank=True, related_name='orders_file')  # Прикрипленные файлы
    pdf_view = models.FileField(default='default.pdf', upload_to='pdf', verbose_name='Обложка заказа pdf')  # Файл обложки заказа PDF
    image_view = models.ImageField(default='default.jpg', upload_to='image_preview', verbose_name='Обложка заказа image')
    other_files = models.FileField(default='default.jpg', upload_to='otherFiles')  # Другие файлы заказа
    amount = models.PositiveIntegerField(verbose_name='Кол-во изделий')  # Кол-во изделий
    city = models.ForeignKey(AllCity, on_delete=models.PROTECT, verbose_name='Город заказа')  # Город заказа
    lead_time = models.DateField(verbose_name='Срок выполнения')  # Срок выполнения заказа
    proposed_budget = models.CharField(max_length=40, choices=BUDGET_EXAMPLE, default='Неизвестный',
                                       verbose_name='Бюджет')  # Предложеный бюджет
    activity = models.BooleanField()  # Активность заказа
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='В обсуждении',
                              verbose_name='Статус заказа')  # Статус заказ
    categories = models.ManyToManyField('OperationCategories', blank=True, related_name='orders',
                                        verbose_name='Категории')

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


class File(models.Model):
    file = models.FileField(upload_to='files', blank=True, null=True, verbose_name='Файл')
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Файлы'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.file.name


class Suggestion(models.Model):

    SUGGESTION_STATUS = (
        ('В обсуждении', 'В обсуждении'),
        ('В работe', 'В работe'),
        ('Выполнено', 'Выполнено'),
        ('Отклонено', 'Отклонено'),
    )

    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    date_create = models.DateTimeField(default=timezone.now)
    offer_description = models.TextField()
    deadline = models.DateTimeField()
    offer_price = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=SUGGESTION_STATUS, default='В обсуждении',
                              verbose_name='Статус предложения')
    selected_offer = models.BooleanField()

    def __str__(self):
        return self.offer_description
