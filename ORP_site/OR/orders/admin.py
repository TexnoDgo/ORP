from django.contrib import admin
from .models import Order, OperationCategories, Suggestion, AllCity, File, MassOrder

admin.site.register(Order)
admin.site.register(OperationCategories)
admin.site.register(Suggestion)
admin.site.register(AllCity)
admin.site.register(File)
admin.site.register(MassOrder)


# Register your models here.
