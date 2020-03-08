from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from .models import Order
from .forms import OrderCreateForm
from django.contrib import messages


def orders(request):
    all_orders = Order.objects.all()
    context = {
        'all_orders': all_orders
    }
    return render(request, 'orders/all_orders.html', context)


class OrderListView(ListView):
    model = Order
    template_name = 'orders/all_orders.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'order'
    ordering = ['-date_ordered']


def order_create(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.author = request.user
            order.save()
            #form.save()  # Сохранение  формы
            title = form.cleaned_data.get('title')  # Получение названи заказка из формы
            messages.success(request,
                             f'You order has been created!Wait for a response! ')  # Формирование сообщения со вложенным именем
            return redirect('orders')  # Перенаправление на страницу подтверждения регистрации
    else:
        form = OrderCreateForm()

    return render(request, 'orders/order_create.html', {'form': form})
