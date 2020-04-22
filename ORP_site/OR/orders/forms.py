from django import forms
from .models import Order, Suggestion, File, MassOrder
from django.views.generic import CreateView


class OrderCreateForm(forms.ModelForm):

    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Order
        fields = ['title', 'description', 'amount', 'city', 'lead_time', 'pdf_view', 'image_view', 'proposed_budget',
                  'activity', 'categories', 'files']

        # Привязка авторезированого пользователя к автору заказа
        def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)


class OrderUpdateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['title', 'description', 'amount', 'city', 'lead_time', 'image_view', 'pdf_view', 'proposed_budget',
                  'status', 'categories']


class SuggestionCreateForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['offer_description', 'deadline', 'offer_price']


class GroupCreateOrderForm(forms.ModelForm):
    class Meta:
        model = MassOrder
        fields = ['other_files']

        def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)


class SendOrderForm(forms.Form):
    email = forms.EmailField(label='Введите email')
    fields = ['email']
