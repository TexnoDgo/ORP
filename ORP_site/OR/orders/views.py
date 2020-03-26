from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Order, OperationCategories, Suggestion, Message, AllCity
from .forms import OrderCreateForm, OrderUpdateForm, SuggestionCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator


def orders(request):
    all_orders = Order.objects.all()

    filters = OperationCategories.objects.all()

    all_city = AllCity.objects.all()

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
        'all_city': all_city,
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
        form = OrderCreateForm(request.POST, request.FILES)

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
        c_form = OrderUpdateForm(request.POST, request.FILES)  # РАЗОБРАТСЯ!! Что нужно передать чтобы получить автоза-
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
    fields = ['title', 'description', 'amount', 'city', 'pdf_view', 'lead_time', 'proposed_budget', 'activity',
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
        ord_sug = Suggestion.objects.filter(order_id=a)
        count = 0
        for sug in ord_sug:
            if sug.selected_offer:
                count += 1
        context['true_sug'] = count
        return context


class DeleteOrderView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Order

    success_url = '/'

    def test_func(self):
        order = self.get_object()
        if self.request.user == order.author:
            return True
        return False


class SuggestionView(DetailView):
    model = Suggestion

    def get_context_data(self, **kwargs):
        context = super(SuggestionView, self).get_context_data(**kwargs)
        a = self.object.order.pk
        ord_sug = Suggestion.objects.filter(order_id=a)
        count = 0
        for sug in ord_sug:
            if sug.selected_offer:
                count += 1
        context['true_sug'] = count
        return context


# ---------------------------------------------Функции изминения статусов заказов -------------------------------------
def status_in_work(request, pk):  # Заказ в работе
    suggestion = Suggestion.objects.get(pk=pk)
    print(suggestion)
    order_pk = suggestion.order.pk
    print(order_pk)
    order = Order.objects.get(pk=order_pk)
    print(order)
    stat = suggestion.selected_offer
    if stat:
        suggestion.selected_offer = False
        order.status = 'В обсуждении'
    else:
        suggestion.selected_offer = True
        order.status = 'В работe'
    suggestion.save()
    order.save()
    return redirect(request.META['HTTP_REFERER'])


def status_ready(request, pk):
    order = Order.objects.get(pk=pk)
    if order.status == 'В работe':
        order.status = 'Выполненый'
    else:
        order.status = 'В работe'
    order.save()
    return redirect(request.META['HTTP_REFERER'])

# -----------------------------------------------Конец функций изминения заказов-------------------------------------


def filter_category(request, pk):
    all_orders = Order.objects.filter(categories__in=pk).order_by("-date_create")

    filters = OperationCategories.objects.all()

    all_city = AllCity.objects.all()

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
        'all_city': all_city,
    }
    return render(request, 'orders/filter.html', context)