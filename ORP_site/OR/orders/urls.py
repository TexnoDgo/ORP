from django.views.generic import DetailView
from django.conf.urls import url
from .models import Order


urlpatterns = [
    url(r'^(?P<pk>\d+)$', DetailView.as_view(model=Order, template_name='orders/order.html')),
]
