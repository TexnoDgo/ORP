from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


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
    return render(request, 'users/profile.html')