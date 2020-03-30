from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from HomePage.views import index
from chat import views as chat_views
from users import views as user_views
from orders import views as orders_views
from orders.models import Suggestion, Order

from django.conf.urls import include

urlpatterns = [
    path('', index, name='index'),
    path('register/', user_views.register, name='register'),
    path('all_users/', user_views.UserListViews.as_view(), name='all_users'),
    path('profile/update/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('admin/', admin.site.urls),
    path('orders/', orders_views.orders, name='orders'),
    url(r'orders/filter/(?P<pk>\d+)$', orders_views.filter_category, name='order_category_view'),
    path('order_create/', orders_views.order_create, name='order_create'),
    path('order_create_new/', orders_views.test_order_create, name='order_create_new'),
    path('orders/', include('orders.urls')),
    path('', include('chat.urls')),
    path('conf_reg/', user_views.conf_reg, name='conf_reg'),
    path('account/', include('allauth.urls')),
    path('update/', orders_views.order_update, name='update'),
    url(r'suggestion/(?P<pk>\d+)$', orders_views.suggestion_create, name='suggestion'),
    path('dashboard', include('dashboard.urls')),
    url(r'suggestion/view/(?P<pk>\d+)$', orders_views.SuggestionView.as_view(model=Suggestion,
                                                                        template_name='orders/suggestion_view.html'),
        name='suggestion_detail'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

