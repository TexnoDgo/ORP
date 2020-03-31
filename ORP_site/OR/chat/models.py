from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from orders.models import Suggestion


class Message(models.Model):
    suggestion = models.ForeignKey(Suggestion, verbose_name='Предложение', on_delete=models.CASCADE, default=False)
    member = models.ForeignKey(User, verbose_name='Участник', on_delete=models.CASCADE, default=False)
    message = models.TextField(_("Сообщение"))
    pub_date = models.DateTimeField(_('Дата сообщения'), default=timezone.now)
    is_readed = models.BooleanField(_('Прочитано'), default=False)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message