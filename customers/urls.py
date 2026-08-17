from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list_view, name='customer-list'),
    path('create/', views.customer_create_view, name='customer-create'),
    path('<int:pk>/', views.customer_detail_view, name='customer-detail'),
    path('<int:pk>/update/', views.customer_update_view, name='customer-update'),
    path('<int:pk>/delete/', views.customer_delete_view, name='customer-delete'),
    path('<int:pk>/add-contact/', views.add_contact_view, name='add-contact'),
    path('<int:pk>/add-note/', views.add_note_view, name='add-note'),
]
