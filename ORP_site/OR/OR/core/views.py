from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def singup(request):
    return render(request, 'registration/singup.html')