from django.shortcuts import render
from django.contrib.auth.models import User
from orders.models import Order
from django.core.paginator import Paginator


def index(request):
    user_order = Order.objects.filter(author=request.user)
    count = 0
    for order in user_order:
        count += 1
    context = {
        'user_order': user_order,
        'user_order_count': count
    }
    return render(request, 'dashboard/dashboard.html', context)


def dashboard_order(request):
    order = Order.objects.filter(author=request.user)
    context = {
        'order': order,
    }
    return render(request, 'dashboard/dashboard-order.html', context)


def dashboard_order_dis(request):
    order = Order.objects.filter(author=request.user)

    paginator = Paginator(order, 3)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    context = {
        'order': posts,
    }
    return render(request, 'dashboard/dashboard-order-dis.html', context)
