from django.contrib import admin
from django.urls import path, include
from dashboard.views import landing_page_view

# Django Admin Portal Customization
admin.site.site_header = "Enterprise CRM Administration"
admin.site.site_title = "Enterprise CRM Admin Portal"
admin.site.index_title = "CRM System Governance & Data Management"

urlpatterns = [
    path('', landing_page_view, name='landing-page'),
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('customers/', include('customers.urls')),
    path('leads/', include('leads.urls')),
    path('opportunities/', include('opportunities.urls')),
    path('tasks/', include('tasks.urls')),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
