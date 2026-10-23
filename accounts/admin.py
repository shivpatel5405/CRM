from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('CRM Workspace Profile', {'fields': ('role', 'phone', 'bio')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('CRM Workspace Profile', {'fields': ('role', 'phone', 'bio')}),
    )
    list_display = ('username', 'full_name_display', 'email', 'role_badge', 'phone', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    ordering = ('username',)
    actions = ('make_sales_rep', 'make_manager', 'activate_users', 'deactivate_users')

    @admin.display(description='Full Name')
    def full_name_display(self, obj):
        name = obj.get_full_name()
        return name if name else "—"

    @admin.display(description='Role')
    def role_badge(self, obj):
        colors = {
            User.Role.ADMIN: 'badge-red',
            User.Role.MANAGER: 'badge-amber',
            User.Role.SALES_REP: 'badge-blue',
        }
        color = colors.get(obj.role, 'badge-gray')
        return format_html('<span class="badge-pill {}">{}</span>', color, obj.get_role_display())

    @admin.action(description="Assign selected users as Sales Representative")
    def make_sales_rep(self, request, queryset):
        updated = queryset.update(role=User.Role.SALES_REP)
        self.message_user(request, f"{updated} user(s) assigned as Sales Representative.")

    @admin.action(description="Assign selected users as Manager")
    def make_manager(self, request, queryset):
        updated = queryset.update(role=User.Role.MANAGER)
        self.message_user(request, f"{updated} user(s) assigned as Manager.")

    @admin.action(description="Activate selected users")
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} user(s) successfully activated.")

    @admin.action(description="Deactivate selected users")
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} user(s) successfully deactivated.")
