from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Count, Sum, Q
from .models import Customer, Contact, Note


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0
    fields = ('first_name', 'last_name', 'email', 'phone', 'designation', 'is_primary')


class NoteInline(admin.TabularInline):
    model = Note
    extra = 0
    fields = ('author', 'content', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'company',
        'email',
        'phone',
        'status_badge',
        'contacts_count_display',
        'opportunities_summary',
        'assigned_to',
        'created_at'
    )
    list_filter = ('status', 'assigned_to', 'created_at')
    search_fields = ('name', 'company', 'email', 'phone')
    date_hierarchy = 'created_at'
    autocomplete_fields = ('assigned_to',)
    inlines = [ContactInline, NoteInline]
    actions = ('mark_active', 'mark_inactive')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            contacts_total=Count('contacts', distinct=True),
            deals_total=Count('opportunities', distinct=True),
            won_revenue=Sum('opportunities__amount', filter=Q(opportunities__stage='CLOSED_WON'))
        )

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {
            Customer.Status.ACTIVE: 'badge-green',
            Customer.Status.LEAD: 'badge-blue',
            Customer.Status.INACTIVE: 'badge-gray',
        }
        color = colors.get(obj.status, 'badge-gray')
        return format_html('<span class="badge-pill {}">{}</span>', color, obj.get_status_display())

    @admin.display(description='Contacts', ordering='contacts_total')
    def contacts_count_display(self, obj):
        count = getattr(obj, 'contacts_total', 0)
        return format_html('<strong>{}</strong> contact(s)', count)

    @admin.display(description='Won Revenue', ordering='won_revenue')
    def opportunities_summary(self, obj):
        revenue = getattr(obj, 'won_revenue', 0.00) or 0.00
        formatted = f"${float(revenue):,.0f}"
        return format_html('<span class="metric-highlight">{}</span>', formatted)

    @admin.action(description="Mark selected customers as ACTIVE")
    def mark_active(self, request, queryset):
        updated = queryset.update(status=Customer.Status.ACTIVE)
        self.message_user(request, f"{updated} customer(s) marked as Active.")

    @admin.action(description="Mark selected customers as INACTIVE")
    def mark_inactive(self, request, queryset):
        updated = queryset.update(status=Customer.Status.INACTIVE)
        self.message_user(request, f"{updated} customer(s) marked as Inactive.")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'designation', 'customer', 'primary_badge', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'customer__name')
    autocomplete_fields = ('customer',)
    actions = ('mark_as_primary',)

    @admin.display(description='Name')
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    @admin.display(description='Primary')
    def primary_badge(self, obj):
        if obj.is_primary:
            return mark_safe('<span class="badge-pill badge-green">Primary</span>')
        return mark_safe('<span class="text-muted">—</span>')

    @admin.action(description="Mark selected contacts as Primary")
    def mark_as_primary(self, request, queryset):
        updated = queryset.update(is_primary=True)
        self.message_user(request, f"{updated} contact(s) marked as primary.")


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('content_preview', 'author', 'related_entity', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'customer__name', 'lead__title')
    date_hierarchy = 'created_at'

    @admin.display(description='Note Content')
    def content_preview(self, obj):
        return (obj.content[:75] + '...') if len(obj.content) > 75 else obj.content

    @admin.display(description='Linked Entity')
    def related_entity(self, obj):
        if obj.customer:
            return format_html('🏢 Customer: <strong>{}</strong>', obj.customer.name)
        elif obj.lead:
            return format_html('🎯 Lead: <strong>{}</strong>', obj.lead.title)
        elif obj.opportunity:
            return format_html('💼 Deal: <strong>{}</strong>', obj.opportunity.name)
        return "—"
