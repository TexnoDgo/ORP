from django.contrib import admin
from django.urls import path
from HomePage.views import index
from users import views as user_views

urlpatterns = [
    path('', index, name='index'),
    path('register/', user_views.register, name='register'),
    path('admin/', admin.site.urls),
]
