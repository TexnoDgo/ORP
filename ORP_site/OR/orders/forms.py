from django import forms
from .models import Order, Suggestion
from django.views.generic import CreateView


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'description', 'amount', 'city', 'lead_time', 'pdf_view', 'proposed_budget', 'activity',
                  'categories']

        # Привязка авторезированого пользователя к автору заказа
        def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)


class FileForm(forms.ModelForm):
    class Meta:
        pass


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'description', 'amount', 'city', 'lead_time', 'pdf_view', 'proposed_budget', 'status',
                  'categories']


class SuggestionCreateForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['date_create', 'offer_description', 'deadline', 'offer_price', 'status', 'selected_offer']

