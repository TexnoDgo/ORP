from django.contrib import admin
from .models import Order, OperationCategories, Suggestion, Message, AllCity

admin.site.register(Order)
admin.site.register(OperationCategories)
admin.site.register(Suggestion)
admin.site.register(Message)
admin.site.register(AllCity)

# Register your models here.
