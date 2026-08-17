from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list_view, name='task-list'),
    path('create/', views.task_create_view, name='task-create'),
    path('<int:pk>/', views.task_detail_view, name='task-detail'),
    path('<int:pk>/update/', views.task_update_view, name='task-update'),
    path('<int:pk>/delete/', views.task_delete_view, name='task-delete'),
    path('<int:pk>/toggle/', views.toggle_task_status_view, name='task-toggle'),
]
