from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('title', 'first_name', 'last_name', 'company', 'status', 'source', 'priority', 'assigned_to', 'estimated_value')
    list_filter = ('status', 'source', 'priority', 'assigned_to')
    search_fields = ('title', 'first_name', 'last_name', 'company', 'email')
