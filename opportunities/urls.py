from django.urls import path
from . import views

urlpatterns = [
    path('', views.opportunity_list_view, name='opportunity-list'),
    path('create/', views.opportunity_create_view, name='opportunity-create'),
    path('<int:pk>/', views.opportunity_detail_view, name='opportunity-detail'),
    path('<int:pk>/update/', views.opportunity_update_view, name='opportunity-update'),
    path('<int:pk>/delete/', views.opportunity_delete_view, name='opportunity-delete'),
]
