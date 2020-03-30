from django.views.generic import DetailView
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^dialogs/$', login_required(views.DialogsView.as_view()), name='dialogs'),
    url(r'^dialogs/create/(?P<user_id>\d+)/$', login_required(views.CreateDialogView.as_view()), name='create_dialog'),
    url(r'^dialogs/(?P<chat_id>\d+)/$', login_required(views.MessagesView.as_view()), name='messages'),
]