from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_list_view, name='lead-list'),
    path('pipeline/', views.lead_pipeline_view, name='lead-pipeline'),
    path('create/', views.lead_create_view, name='lead-create'),
    path('<int:pk>/', views.lead_detail_view, name='lead-detail'),
    path('<int:pk>/update/', views.lead_update_view, name='lead-update'),
    path('<int:pk>/delete/', views.lead_delete_view, name='lead-delete'),
    path('<int:pk>/convert/', views.convert_lead_to_customer_view, name='lead-convert'),
]
