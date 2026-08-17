from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('dashboard'), name='root-redirect'),
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('customers/', include('customers.urls')),
    path('leads/', include('leads.urls')),
    path('opportunities/', include('opportunities.urls')),
    path('tasks/', include('tasks.urls')),
]
