from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Order, OperationCategories, Suggestion, AllCity, File, MassOrder
from .forms import OrderCreateForm, SuggestionCreateForm, GroupCreateOrderForm, SendOrderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator

import zipfile
import os

from chat.models import Message
from chat.forms import MessageCreateForm

from users.models import Profile

from .handlers import convert_pdf_to_bnp


# --------------------------------------------------Отображение всех заказов--------------------------------------
def orders(request):
    all_orders = Order.objects.all().order_by('-date_create')

    filters = OperationCategories.objects.all()

    all_city = AllCity.objects.all()

    paginator = Paginator(all_orders, 4)

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
# --------------------------------------------------Отображение всех заказов--------------------------------------


# ------------------------------------------------------Создание заказа-------------------------------------------
@login_required
def order_create(request):
    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.author = request.user
            print(order_form.save().pk)
            print(order.pdf_view.path)
            pdf_file_name = str(order.pdf_view)
            print(pdf_file_name)
            png_file_name = '{}{}'.format(pdf_file_name[4:-3], 'png')
            png_full_path = 'C:/PP/ORP/ORP_site/OR/media/image_preview/' + png_file_name
            print(png_file_name)
            print(png_full_path)
            convert_pdf_to_bnp(order.pdf_view.path, png_full_path)
            order.image_view = png_full_path
            print(order.image_view.path)
            order.save()
            if files:
                for f in files:
                    print(f)
                    fl = File(order=Order.objects.get(pk=order.id), file=f)
                    fl.save()
            order.save()
            # form.save()  # Сохранение  формы
            title = order_form.cleaned_data.get('title')  # Получение названи заказка из формы
            messages.success(request,
                             f'You order has been created!Wait for a response! ')  # Формирование сообщения со вложенным именем
            return redirect('orders')  # Перенаправление на страницу подтверждения регистрации
    else:
        order_form = OrderCreateForm()

    return render(request, 'orders/order_create.html', {'order_form': order_form})
# ------------------------------------------------------Создание заказа-------------------------------------------


@login_required
def add_order_archive(request):
    if request.method == 'POST':
        form = GroupCreateOrderForm(request.POST, request.FILES)
        if form.is_valid():
            archive = form.save(commit=False)
            archive.author = request.user
            form.save()
            return redirect('/order/view_archives')

    else:
        form = GroupCreateOrderForm()

    context = {
        'form': form
    }
    return render(request, 'orders/add_order_archive.html', context)


@login_required
def view_archives(request):
    all_user_archive = MassOrder.objects.filter(author=request.user)
    context = {
        'form': all_user_archive,
    }
    return render(request, 'orders/view_archives.html', context)


@login_required
def create_many_order(request, pk):
    archive_files = MassOrder.objects.get(pk=pk)
    open_archive = zipfile.ZipFile(archive_files.other_files, 'r')
    archive_path = 'C:/PP/ORP/ORP_site/OR/media/temp/' + str(archive_files)
    list_files = list()
    for name in open_archive.namelist():
        print(name)
        list_files.append(name)
        print(list_files)
        open_archive.extract(name)
        os.rename(name, name.decode('cp866'))

    os.removedirs(list_files[0])
    return render(request, 'orders/create_many_order.html')


# ------------------------------------------------------Обновление заказа-------------------------------------------
class OrderUpdateView(UpdateView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        a = self.object.id
        context['files'] = File.objects.filter(order=a)
        return context

    fields = ['title', 'description', 'amount', 'city', 'image_view', 'pdf_view', 'lead_time', 'proposed_budget',
              'activity', 'status', 'categories']

    def form_valid(self, form):
        form.instance.author = self.request.user
        order = form.save(commit=False)
        pdf_file_name = str(order.pdf_view)
        print(pdf_file_name)
        png_file_name = '{}{}'.format(pdf_file_name[4:-3], 'png')
        png_full_path = 'C:/PP/ORP/ORP_site/OR/media/image_preview/' + png_file_name
        print(png_file_name)
        print(png_full_path)
        convert_pdf_to_bnp(order.pdf_view.path, png_full_path)
        order.image_view = png_full_path
        print(order.image_view.path)
        order.save()
        return super().form_valid(form)
# ------------------------------------------------------Обновление заказа-------------------------------------------


# -----------------------------------------------Фильтр заказов-------------------------------------------------
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


def filter_category(request, pk):
    all_orders = Order.objects.filter(categories__in=pk).order_by("-date_create")

    filters = OperationCategories.objects.all()

    filCat = OperationCategories.objects.get(pk=pk)

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
        'filCat': filCat,
    }
    return render(request, 'orders/filter.html', context)


def filter_city(request, pk):
    all_orders = Order.objects.filter(city=pk).order_by("-date_create")

    filters = OperationCategories.objects.all()

    filcit = AllCity.objects.get(pk=pk)

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
        'filcit': filcit,
    }
    return render(request, 'orders/filter.html', context)
# -----------------------------------------------Фильтр заказов по категориям-------------------------------------


# -----------------------------------------------Создание предложения-------------------------------------
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
# -----------------------------------------------Создание предложения-------------------------------------


class OrderAndSuggestionView(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderAndSuggestionView, self).get_context_data(**kwargs)
        a = self.object.id
        context['suggestions'] = Suggestion.objects.filter(order_id=a)
        context['files'] = File.objects.filter(order_id=a)
        context['all_suggestions'] = Suggestion.objects.all()
        context['profiles'] = Profile.objects.all()
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
        sug_mes = Message.objects.filter(suggestion_id=a)
        ord_sug = Suggestion.objects.filter(order_id=a)
        count = 0
        for sug in ord_sug:
            if sug.selected_offer:
                count += 1
        context['true_sug'] = count
        context['messages'] = sug_mes
        return context


# ---------------------------------------------Функции изминения статусов заказов -------------------------------------
def status_in_work(request, pk):  # Заказ в работе
    suggestion = Suggestion.objects.get(pk=pk)
    order_pk = suggestion.order.pk
    order = Order.objects.get(pk=order_pk)
    stat = suggestion.selected_offer
    if stat:
        suggestion.selected_offer = False
        order.status = 'В обсуждении'
        suggestion.status = 'В обсуждении'
    else:
        suggestion.selected_offer = True
        order.status = 'В работe'
        suggestion.status = 'В работe'
    suggestion.save()
    order.save()
    return redirect(request.META['HTTP_REFERER'])


def status_ready(request, pk):
    order = Order.objects.get(pk=pk)
    selected_suggestion = Suggestion.objects.get(order__pk=pk, selected_offer=True)
    if order.status == 'В работe':
        order.status = 'Выполненый'
        selected_suggestion.status = 'Выполнено'
    else:
        order.status = 'В работe'
        selected_suggestion.status = 'В работe'
    selected_suggestion.save()
    order.save()
    return redirect(request.META['HTTP_REFERER'])
# ------------------------------------------Конец функций изминения статуса заказов-------------------------------------


# ---------------------------------------------Функции изминения рейтинга заказов -------------------------------------
# Оценка "1"
def get_one_rating(request, pk):
    print(pk)
    suggestion = Suggestion.objects.get(pk=pk)
    sug_user_profile = Profile.objects.get(user=suggestion.author)
    print(sug_user_profile)
    print(suggestion)
    print(suggestion.rating)
    if suggestion.rating == 0:
        suggestion.rating = 1
        sug_user_profile.rating += 1
    suggestion.save()
    sug_user_profile.save()
    print(suggestion.rating)
    return redirect(request.META['HTTP_REFERER'])


# Оценка "2"
def get_two_rating(request, pk):
    suggestion = Suggestion.objects.get(pk=pk)
    sug_user_profile = Profile.objects.get(user=suggestion.author)
    print(sug_user_profile)
    if suggestion.rating == 0:
        suggestion.rating = 2
        sug_user_profile.rating += 2
    suggestion.save()
    sug_user_profile.save()
    print(suggestion.rating)
    return redirect(request.META['HTTP_REFERER'])


# Оценка "3"
def get_three_rating(request, pk):
    suggestion = Suggestion.objects.get(pk=pk)
    sug_user_profile = Profile.objects.get(user=suggestion.author)
    print(sug_user_profile)
    if suggestion.rating == 0:
        suggestion.rating = 3
        sug_user_profile.rating += 3
    suggestion.save()
    sug_user_profile.save()
    print(suggestion.rating)
    return redirect(request.META['HTTP_REFERER'])


# Оценка "4"
def get_four_rating(request, pk):
    suggestion = Suggestion.objects.get(pk=pk)
    sug_user_profile = Profile.objects.get(user=suggestion.author)
    print(sug_user_profile)
    if suggestion.rating == 0:
        suggestion.rating = 4
        sug_user_profile.rating += 4
    suggestion.save()
    sug_user_profile.save()
    print(suggestion.rating)
    return redirect(request.META['HTTP_REFERER'])


# Оценка "5"
def get_five_rating(request, pk):
    suggestion = Suggestion.objects.get(pk=pk)
    sug_user_profile = Profile.objects.get(user=suggestion.author)
    print(sug_user_profile)
    if suggestion.rating == 0:
        suggestion.rating = 5
        sug_user_profile.rating += 5
    suggestion.save()
    sug_user_profile.save()
    print(suggestion.rating)
    return redirect(request.META['HTTP_REFERER'])

# -----------------------------------------------Конец функций изминения заказов-------------------------------------


# Отправка заказа другу
@login_required
def send_order_to_friend(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        form = SendOrderForm(request.POST)
        return redirect('orders')
    else:
        form = SendOrderForm()
    print(form)
    context = {
        'order': order,
        'form': form,
    }
    return render(request, 'orders/send_order_to_friend.html', context)

