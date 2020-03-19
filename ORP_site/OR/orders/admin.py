from django.contrib import admin
from .models import Order, OperationCategories, Suggestion, Message

admin.site.register(Order)
admin.site.register(OperationCategories)
admin.site.register(Suggestion)
admin.site.register(Message)

# Register your models here.
