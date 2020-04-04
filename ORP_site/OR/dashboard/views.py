from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator

from django.contrib.auth.models import User
from orders.models import Order, Suggestion
from chat.models import Message

from chat.forms import MessageCreateForm




def index(request):
    user_order = Order.objects.filter(author=request.user)

    count = 0
    count2 = 0
    count3 = 0
    count4 = 0
    for order in user_order:
        count += 1
        if order.status == 'В работe':
            count2 += 1
        elif order.status == 'Выполненый':
            count3 += 1
        elif order.status == 'В обсуждении':
            count4 += 1

    context = {
        'user_order': user_order,
        'user_order_count': count,
        'user_order_count_in_work': count2,
        'user_order_count_ready': count3,
        'user_order_count_dis': count4,
    }
    return render(request, 'dashboard/dashboard.html', context)


def dashboard_order(request):
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


def dashboard_order_ready(request):
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
    return render(request, 'dashboard/dashboard-order-ready.html', context)


def dashboard_sug_active(request):

    suggestions = Suggestion.objects.filter(author=request.user)

    orders = Order.objects.all()

    paginator = Paginator(suggestions, 3)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    context = {
        'suggestions': posts,
        'orders': orders,
    }
    return render(request, 'dashboard/dashboard-sug-active.html', context)


def dialogsView(request):
    suggestions = Suggestion.objects.filter(author=request.user)

    context = {
        'suggestions': suggestions,
    }
    return render(request, 'dashboard/dashboard-messages.html', context)


def messages(request, pk):
    suggestions = Suggestion.objects.filter(author=request.user)
    suggestion = Suggestion.objects.get(pk=pk)
    suggestion_order = Order.objects.get(pk=suggestion.order.pk)
    if request.method == 'POST':
        form = MessageCreateForm(request.POST)
        if form.is_valid():
            mes_form = form.save(commit=False)
            mes_form.suggestion = suggestion
            # Выбор автора сообщения
            mes_form.member = request.user
            mes_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = MessageCreateForm()

    message = Message.objects.filter(suggestion_id=pk)

    context = {
        'message1': message,
        'suggestions': suggestions,
        'suggestion': suggestion,
        'form': form,
        'suggestion_order': suggestion_order,
    }
    return render(request, 'dashboard/dashboard-message-view.html', context)
