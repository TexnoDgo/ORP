from django.views.generic import DetailView
from django.conf.urls import url
from django.urls import path, re_path
from .views import index, dashboard_order, dashboard_order_dis, dashboard_order_ready, dashboard_sug_active, dialogsView
from orders import views
from orders.models import Order

urlpatterns = [
    path('', index, name='dashboard'),

    path('/dashboard-order', dashboard_order, name='dashboard-order'),
    path('/dashboard-order/dis', dashboard_order_dis, name='dashboard-order-dis'),
    path('/dashboard-order/ready', dashboard_order_ready, name='dashboard_order_ready'),

    path('/dashboard-messages', dialogsView, name='dashboard-messages'),

    path('/dashboard-sug/active', dashboard_sug_active, name='dashboard_sug_active'),

    re_path('/dashboard-order/(?P<pk>\d+)$', views.OrderAndSuggestionView.as_view(model=Order,
                                                                                  template_name='orders/order.html'),
            name='order_detail'),
]
