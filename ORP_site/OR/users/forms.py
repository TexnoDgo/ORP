from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, CompanyProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class CompanyProfileCreateForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        #fields = ['user', 'name', 'edrpou', 'officialName', 'address', 'mainPerson', 'occupation', 'status']
        fields = ['edrpou']

        # Привязка авторезированого пользователя к автору заказа
        def form_valid(self, form):
            form.instance.user_name = self.request.user
            return super().form_valid(form)
