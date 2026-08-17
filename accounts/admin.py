from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('CRM Profile Info', {'fields': ('role', 'phone', 'bio')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('CRM Profile Info', {'fields': ('role', 'phone', 'bio')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
