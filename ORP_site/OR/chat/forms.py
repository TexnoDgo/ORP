from django import forms
from .models import Message


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']