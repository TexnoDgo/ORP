from django.contrib import admin
from .models import Order, OperationCategories, Suggestion

admin.site.register(Order)
admin.site.register(OperationCategories)
admin.site.register(Suggestion)

# Register your models here.
