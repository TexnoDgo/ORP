from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CompanyProfileCreateForm
from django.contrib.auth.models import User
import requests
import json


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        #  Сообщение об успешной регистрации
        if form.is_valid():
            form.save()  # Сохранение  формы
            username = form.cleaned_data.get('username')  # Получение имени из формы
            messages.success(request, f'You account has been created! You are now able to log in')  # Формирование сообщения со вложенным именем
            return redirect('conf_reg')  # Перенаправление на страницу подтверждения регистрации
    else:
        form = UserRegisterForm()
    return render(request, 'users/singup.html', {'form': form})


def conf_reg(request):
    return render(request, 'users/conf_reg.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,
                             f'Your account has been update!')  # Формирование сообщения Alert
            return redirect('profile')  # Перенаправление на страницу Профиля

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


class UserListViews(ListView):
    model = User


def createCompanyProfile(request):
    if request.method == 'POST':
        form = CompanyProfileCreateForm(request.POST)

        if form.is_valid():
            company_profile = form.save(commit=False)

            # -----API-----
            empty_field = 'edrpou'
            value = company_profile.edrpou
            print(value)
            prelink = '{%22' + empty_field + '%22:%22' + value + '%22}'
            print(prelink)
            link = 'http://edr.data-gov-ua.org/api/companies?where=' + prelink
            print('link:' + link)
            response = requests.get(link)
            data = json.loads(response.text)
            print(data)
            first = data[0]
            print(first)
            # -----API-----
            company_profile.user_name = request.user
            company_profile.name = first["name"]
            company_profile.officialName = first["officialName"]
            company_profile.address = first["address"]
            company_profile.mainPerson = first["mainPerson"]
            company_profile.occupation = first["occupation"]
            company_profile.status = first["status"]
            company_profile.save()

            return redirect('orders')
    else:
        form = CompanyProfileCreateForm()
    return render(request, 'users/company_profile_create.html', {'form': form})
