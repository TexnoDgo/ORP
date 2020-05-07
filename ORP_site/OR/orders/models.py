from datetime import date

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class AllCity(models.Model):
    title = models.CharField(max_length=50, default=_('not_selected'))

    objects = models.Manager()

    def __str__(self):
        return self.title


class MassOrder(models.Model):
    BUDGET_EXAMPLE = (
        (_('Unknown'), _('Unknown')),
        (_('Small, less than $ 100'), _('Small, less than $ 100')),
        (_('Medium, less than $ 1000'), _('Medium, less than $ 1000')),
        (_('High, over $ 1000'), _('High, over $ 1000'))
    )

    ORDER_STATUS = (
        (_('In discussion'), _('In discussion')),
        (_('In work'), _('In work')),
        (_('Done'), _('Done')),
        (_('Canceled'), _('Canceled')),
    )
    author = models.ForeignKey(User, on_delete=models.PROTECT)  # Автор заказа. Автоматически
    date_create = models.DateTimeField(default=timezone.now)  # Время создания заказа. Автоматически
    other_files = models.FileField(upload_to='MassOrderArchive', verbose_name=_('Archive'))  # Другие файлы заказа
    title = models.CharField(max_length=100, verbose_name=_('Headline'), default=_('Headline'))  # Заголовок заказа
    description = models.TextField(verbose_name=_('Description Order'),
                                   default=_('Description Order'))  # Описание заказа
    city = models.ForeignKey(AllCity, on_delete=models.PROTECT, verbose_name=_('Order City'),
                             null=True)  # Город заказа
    lead_time = models.DateField(verbose_name=_('Deadline'), default=timezone.now)  # Срок выполнения заказа
    proposed_budget = models.CharField(max_length=40, choices=BUDGET_EXAMPLE, default=_('Unknown'),
                                       verbose_name=_('Budget'))  # Предложеный бюджет
    activity = models.BooleanField(default=False)  # Активность заказа
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default=_('In discussion'),
                              verbose_name=_('Order status'))  # Статус заказ
    crushed_order = models.BooleanField(default=False)

    def __str__(self):
        return 'GroupOrder -' + str(self.title)


class Order(models.Model):
    BUDGET_EXAMPLE = (
        (_('Unknown'), _('Unknown')),
        (_('Small, less than $ 100'), _('Small, less than $ 100')),
        (_('Medium, less than $ 1000'), _('Medium, less than $ 1000')),
        (_('High, over $ 1000'), _('High, over $ 1000'))
    )

    ORDER_STATUS = (
        (_('In discussion'), _('In discussion')),
        (_('In work'), _('In work')),
        (_('Done'), _('Done')),
        (_('Canceled'), _('Canceled')),
    )
    id = models.AutoField(primary_key=True)
    mass_order = models.ForeignKey(MassOrder, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)  # Автор заказа. Автоматически
    date_create = models.DateTimeField(default=timezone.now)  # Время создания заказа. Автоматически
    title = models.CharField(max_length=100, verbose_name=_('Headline'), default=_('Headline'))  # Заголовок заказа
    description = models.TextField(verbose_name=_('Description Order'),
                                   default=_('Description Order'))  # Описание заказа
    # Файл обложки заказа PDF
    pdf_view = models.FileField(default='default.pdf',
                                upload_to='pdf',
                                verbose_name=_('Pdf order cover'))
    # Файл обложки заказа Jpeg
    image_view = models.ImageField(default='default.jpg',
                                   upload_to='image_preview',
                                   verbose_name=_('Cover image'))
    amount = models.PositiveIntegerField(default=1, verbose_name=_('Number of products'))  # Кол-во изделий
    city = models.ForeignKey(AllCity, on_delete=models.PROTECT, verbose_name=_('Order City'),
                             null=True)  # Город заказа
    lead_time = models.DateField(verbose_name=_('Deadline'), default=timezone.now)  # Срок выполнения заказа
    proposed_budget = models.CharField(max_length=40, choices=BUDGET_EXAMPLE, default=_('Unknown'),
                                       verbose_name=_('Budget'))  # Предложеный бюджет
    activity = models.BooleanField(default=False)  # Активность заказа
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default=_('In discussion'),
                              verbose_name=_('Order status'))  # Статус заказ
    categories = models.ManyToManyField('OperationCategories', blank=True, related_name='orders',
                                        verbose_name=_('Categories'), null=True)
    group_order = models.BooleanField(default=False, verbose_name=_('Group?'))

    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})


# --------------------------------Group Order---------------------------------
class Material(models.Model):
    title = models.CharField(max_length=250)

    objects = models.Manager()

    def __str__(self):
        return self.title
# -----------------------------------------------------------------


class OperationCategories(models.Model):
    title = models.CharField(max_length=30)

    objects = models.Manager()

    def __str__(self):
        return self.title


class File(models.Model):
    file = models.FileField(upload_to='files', blank=True, null=True, verbose_name=_('File'))
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Files')
        verbose_name_plural = _('Files')

    def __str__(self):
        return self.file.name


class Suggestion(models.Model):

    SUGGESTION_STATUS = (
        (_('In discussion'), _('In discussion')),
        (_('In work'), _('In work')),
        (_('Done'), _('Done')),
        (_('Canceled'), _('Canceled')),
    )

    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    date_create = models.DateTimeField(default=timezone.now)
    offer_description = models.TextField(verbose_name=_('Offer Description'))
    deadline = models.DateTimeField(verbose_name=_('Production time'))
    offer_price = models.PositiveIntegerField(verbose_name=_('Suggested price'))
    status = models.CharField(max_length=20, choices=SUGGESTION_STATUS, default=_('In discussion'),
                              verbose_name=_('Offer Status'))
    selected_offer = models.BooleanField(default=False)
    rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.offer_description


class GroupSuggestion(models.Model):
    SUGGESTION_STATUS = (
        (_('In discussion'), _('In discussion')),
        (_('In work'), _('In work')),
        (_('Done'), _('Done')),
        (_('Canceled'), _('Canceled')),
    )
    mass_order = models.ForeignKey(MassOrder, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    date_create = models.DateTimeField(default=timezone.now)
    offer_description = models.TextField(verbose_name=_('Offer Description'))
    deadline = models.DateTimeField(verbose_name=_('Production time'))
    offer_price = models.PositiveIntegerField(verbose_name=_('Suggested price'))
    status = models.CharField(max_length=20, choices=SUGGESTION_STATUS, default=_('In discussion'),
                              verbose_name=_('Offer Status'))
    selected_offer = models.BooleanField(default=False)
    rating = models.PositiveIntegerField(default=0)


class Feedback(models.Model):
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    date_create = models.DateField(default=timezone.now)
    feet = models.TextField()

    def __str__(self):
        return self.feet

