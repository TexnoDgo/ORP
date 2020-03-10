from django import forms
from .models import Order
from django.views.generic import CreateView


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'description', 'amount', 'city', 'lead_time', 'proposed_budget', 'activity', 'status', 'categories']

        # Привязка авторезированого пользователя к автору заказа
        def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'description', 'amount', 'city', 'lead_time', 'proposed_budget', 'activity', 'status', 'categories']
