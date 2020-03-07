from django.shortcuts import render
from .models import Order


def orders(request):
    all_orders = Order.objects.all()
    context = {
        'all_orders': all_orders
    }
    return render(request, 'orders/all_orders.html', context)


def order_create(request):
    return render(request, 'orders/order_create.html')