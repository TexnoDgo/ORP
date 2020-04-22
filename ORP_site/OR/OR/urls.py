from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from HomePage.views import index, index2
from chat import views as chat_views
from users import views as user_views
from orders import views as orders_views
from orders.models import Suggestion, Order

from chat import views as chat_views

from django.conf.urls import include

urlpatterns = [
    path('', index, name='index'),
    path('example/', index2, name='index2'),

    path('register/', user_views.register, name='register'),
    path('all_users/', user_views.UserListViews.as_view(), name='all_users'),

    path('profile/update/', user_views.profile_update, name='profile_update'),
    path('profile/view/', user_views.profile_view, name='profile_view'),
    path('profile/CompanyProfile/create', user_views.createCompanyProfile, name='createCompanyProfile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('account/', include('allauth.urls')),
    path('profile/set-up-notifications/', user_views.set_up_notifications, name='set-up-notifications'),

    path('admin/', admin.site.urls),

    path('orders/', orders_views.orders, name='orders'),
    url(r'orders/filter/category/(?P<pk>\d+)$', orders_views.filter_category, name='order_category_view'),
    url(r'orders/filter/city/(?P<pk>\d+)$', orders_views.filter_city, name='order_city_view'),
    path('order_create/', orders_views.order_create, name='order_create'),

    path('order/add_order_archive/', orders_views.add_order_archive, name='add_order_archive'),
    path('order/view_archives', orders_views.view_archives, name='view_archives'),
    url('order/create_many_order/(?P<pk>\d+)$', orders_views.create_many_order, name='create_many_order'),

    #path('order_create_new/', orders_views.test_order_create, name='order_create_new'),
    path('orders/', include('orders.urls')),
    path('', include('chat.urls')),
    path('conf_reg/', user_views.conf_reg, name='conf_reg'),

    url(r'suggestion/(?P<pk>\d+)$', orders_views.suggestion_create, name='suggestion'),

    #url(r'suggestion/view/(?P<pk>\d+)$', orders_views.SuggestionView.as_view(model=Suggestion,
    #                                                                    template_name='orders/suggestion_view.html'),
    #    name='suggestion_detail'),

    url(r'suggestion/view/(?P<pk>\d+)$', chat_views.message_of_suggestion, name='message_and_suggestion'),

    path('dashboard', include('dashboard.urls')),

    url(r'send_order_to_friend/(?P<pk>\d+)$', orders_views.send_order_to_friend, name='send_order_to_friend'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

