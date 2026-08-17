from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_type', 'priority', 'status', 'due_date', 'assigned_to', 'customer', 'lead', 'opportunity')
    list_filter = ('task_type', 'priority', 'status', 'assigned_to', 'due_date')
    search_fields = ('title', 'description')
