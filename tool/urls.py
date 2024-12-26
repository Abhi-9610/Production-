from django.contrib import admin
from django.urls import path
from tools import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('order_list', views.order_form, name='order_form'),
    path('orders/', views.order_list, name='order_list'),
    path('edit/<int:pk>/', views.edit_order, name='edit_order'),  # Edit Order URL
    path('delete/<int:pk>/', views.delete_order, name='delete_order'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)