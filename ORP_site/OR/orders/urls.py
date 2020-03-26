from django.views.generic import DetailView
from django.conf.urls import url
from .models import Order
from django.urls import path
from . import views


urlpatterns = [
    url(r'^(?P<pk>\d+)$', views.OrderAndSuggestionView.as_view(model=Order, template_name='orders/order.html'),
        name='order_detail'),
    path(r'<slug:url>/', views.order_categories, name='order_categories'),
    url(r'^(?P<pk>\d+)/update/', views.OrderUpdateView.as_view(model=Order, template_name='orders/update.html'),
        name='order_update'),
    url(r'^(?P<pk>\d+)/delete/', views.DeleteOrderView.as_view(), name='order_delete'),
    url(r'^(?P<pk>\d+)/status_in_work/', views.status_in_work, name='status_in_work'),
    url(r'^(?P<pk>\d+)/status_ready/', views.status_ready, name='status_ready'),
]