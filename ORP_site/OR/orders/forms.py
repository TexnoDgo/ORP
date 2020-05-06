from django import forms
from .models import Order, Suggestion, File, MassOrder, Detail, Material, GroupOrder
from django.views.generic import CreateView
from django.forms import formset_factory


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


# -------------------------------------------------------------------------------
class GroupCreateOrderForm(forms.ModelForm):
    class Meta:
        model = MassOrder
        fields = ['other_files']

        def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)
# --------------------------------------------------------------------------------


# --------------------------------------------------------------------------------
class DetailCreateForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = ['title', 'file', 'amount', 'categories', 'material', 'note']

        def form_valid(self, form):
            return super().form_valid(form)
# --------------------------------------------------------------------------------


class SendOrderForm(forms.Form):
    email = forms.EmailField(label='Введите email')
    fields = ['email']
