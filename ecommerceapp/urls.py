from django.contrib import admin
from django.urls import path, include

from app.views import product_list, register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register_view, name='register'),
    path('product-list/', product_list, name='product_list'),
]
