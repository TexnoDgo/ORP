from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Order, OperationCategories, Suggestion, Message
from .forms import OrderCreateForm, OrderUpdateForm, SuggestionCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views import generic


def orders(request):
    all_orders = Order.objects.all()

    filters = OperationCategories.objects.all()

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
        'filters': filters,
    }
    return render(request, 'orders/all_orders.html', context)


'''class OrderListView(ListView):
    model = Order
    print(model)
    template_name = 'orders/all_orders.html'
    context_object_name = 'all_orders'
    ordering = ['-date_create']'''


def order_categories(request, url):
    all_orders = Order.objects.filter(categories__url=url)

    filters = OperationCategories.objects.all()

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
        'filters': filters,
    }
    return render(request, 'orders/all_orders.html', context)


'''class OrderListView(ListView):
    model = Order
    template_name = 'orders/all_orders.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'order'
    ordering = ['-date_ordered']'''

@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.author = request.user
            order.save()
            # form.save()  # Сохранение  формы
            title = form.cleaned_data.get('title')  # Получение названи заказка из формы
            messages.success(request,
                             f'You order has been created!Wait for a response! ')  # Формирование сообщения со вложенным именем
            return redirect('orders')  # Перенаправление на страницу подтверждения регистрации
    else:
        form = OrderCreateForm()

    return render(request, 'orders/order_create.html', {'form': form})


@login_required
def order_update(request):
    if request.method == 'POST':
        c_form = OrderUpdateForm(request.POST)  # РАЗОБРАТСЯ!! Что нужно передать чтобы получить автоза-
        # полнение формы.

        if c_form.is_valid():
            c_form.save()
            messages.success(request,
                             f'Order № {{ order.id }} is Update!')  # Формирование сообщения Alert
            return redirect('orders')  # Перенаправление на страницу Заказов
    else:
        c_form = OrderUpdateForm()

    context = {
        'c_form': c_form
    }

    return render(request, 'orders/update.html', context)


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['title', 'description', 'amount', 'city', 'lead_time', 'proposed_budget', 'activity',
              'status', 'categories']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def test_order_create(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.author = request.user
            order.save()
            # form.save()  # Сохранение  формы
            title = form.cleaned_data.get('title')  # Получение названи заказка из формы
            messages.success(request,
                             f'You order has been created!Wait for a response! ')  # Формирование сообщения со вложенным именем
            return redirect('orders')  # Перенаправление на страницу подтверждения регистрации
    else:
        form = OrderCreateForm()

    return render(request, 'orders/order_create_new.html', {'form': form})


@login_required
def suggestion_create(request, pk):
    if request.method == 'POST':
        suggestion = SuggestionCreateForm(request.POST)
        if suggestion.is_valid():
            sug = suggestion.save(commit=False)
            sug.author = request.user
            sug.order = Order.objects.get(pk=pk)
            sug.save()
            # form.save()  # Сохранение  формы
            title = suggestion.cleaned_data.get('title')  # Получение названи заказка из формы
            messages.success(request,
                             f'You suggestion has been created!Wait for a response! ')  # Формирование сообщения со вложенным именем
            return redirect('orders')  # Перенаправление на страницу подтверждения регистрации
    else:
        suggestion = SuggestionCreateForm()

    return render(request, 'orders/suggestion_create.html', {'suggestion': suggestion})


class OrderAndSuggestionView(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderAndSuggestionView, self).get_context_data(**kwargs)
        a = self.object.id
        context['suggestions'] = Suggestion.objects.filter(order_id=a)
        return context


class DeleteOrderView(DeleteView):
    model = Order


class SuggestionView(DetailView):
    model = Suggestion


def change_status(request, pk):
    suggestion = Suggestion.objects.get(pk=pk)
    stat = suggestion.selected_offer
    if stat:
        suggestion.selected_offer = False
    else:
        suggestion.selected_offer = True
    suggestion.save()
    return redirect(request.META['HTTP_REFERER'])


def filter_category(request, pk):
    all_orders = Order.objects.filter(categories__in=pk).order_by("-date_create")

    filters = OperationCategories.objects.all()

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
        'filters': filters,
    }
    return render(request, 'orders/filter.html', context)