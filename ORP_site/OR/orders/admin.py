from django.contrib import admin
from .models import Order, OperationCategories, Suggestion, Message, AllCity, File

admin.site.register(Order)
admin.site.register(OperationCategories)
admin.site.register(Suggestion)
admin.site.register(Message)
admin.site.register(AllCity)
admin.site.register(File)

# Register your models here.
