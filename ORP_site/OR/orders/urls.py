from django.views.generic import DetailView
from django.conf.urls import url
from .models import Order
from django.urls import path
from . import views


urlpatterns = [
    url(r'^(?P<pk>\d+)$', views.OrderAndSuggestionView.as_view(model=Order, template_name='orders/order.html')),
    path(r'<slug:url>/', views.order_categories, name='order_categories'),
    #url(r'^(?P<pk>\d+)/update/', views.OrderUpdateView.as_view(), name='order-update'), #template_name='orders/update.html'
]