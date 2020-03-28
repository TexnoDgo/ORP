from django.shortcuts import render
from django.views.generic import DetailView
from .models import Chat


class DialogsView(DetailView):
    def get(self, request):
        chats = Chat.objects.filter(members__in=[request.user.id])
        return render(request, 'users/dialogs.html', {'user_profile': request.user, 'chats': chats})