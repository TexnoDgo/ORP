from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from .models import Order, OperationCategories
from .forms import OrderCreateForm, OrderUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def orders(request):
    all_orders = Order.objects.all()

    paginator = Paginator(all_orders, 3)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)
    context = {
        'all_orders': posts,
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


@login_required
def order_update(request):
    old_form = Order.objects.filter(author=request.user).first()
    if request.method == 'POST':
        c_form = OrderUpdateForm(request.POST, instance=old_form)  # РАЗОБРАТСЯ!! Что нужно передать чтобы получить автоза-
                                                                # полнение формы.
        if c_form.is_valid():
            c_form.save()
            messages.success(request,
                             f'Order № {{ order.id }} is Update!')  # Формирование сообщения Alert
            return redirect('orders')  # Перенаправление на страницу Заказов
    else:
        c_form = OrderUpdateForm(instance=old_form)

    context = {
        'c_form': c_form
    }

    return render(request, 'orders/update.html', context)


def test_order_create(request):
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

    return render(request, 'orders/order_create_new.html', {'form': form})