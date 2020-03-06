from django.shortcuts import render
from django.utils.translation import ugettext as _


def index(requests):
    return render(requests, 'HomePage/HomePage.html')
