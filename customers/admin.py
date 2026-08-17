from django.contrib import admin
from .models import Customer, Contact, Note


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


class NoteInline(admin.TabularInline):
    model = Note
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'assigned_to', 'created_at')
    search_fields = ('name', 'company', 'email', 'phone')
    inlines = [ContactInline, NoteInline]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'customer', 'is_primary')
    list_filter = ('is_primary', 'customer')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'customer', 'lead', 'opportunity', 'created_at')
    list_filter = ('created_at', 'author')
