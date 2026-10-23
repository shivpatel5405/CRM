from django.contrib import admin
from django.utils.html import format_html
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'contact_person',
        'company',
        'status_badge',
        'priority_badge',
        'formatted_value',
        'source',
        'assigned_to',
        'created_at'
    )
    list_filter = ('status', 'priority', 'source', 'assigned_to', 'created_at')
    search_fields = ('title', 'first_name', 'last_name', 'company', 'email', 'phone')
    date_hierarchy = 'created_at'
    autocomplete_fields = ('assigned_to',)
    actions = ('advance_to_qualified', 'advance_to_proposal', 'mark_as_won', 'mark_as_lost')

    @admin.display(description='Contact')
    def contact_person(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    @admin.display(description='Status', ordering='status')
    def status_badge(self, obj):
        colors = {
            Lead.Status.NEW: 'badge-cyan',
            Lead.Status.CONTACTED: 'badge-blue',
            Lead.Status.QUALIFIED: 'badge-purple',
            Lead.Status.PROPOSAL: 'badge-amber',
            Lead.Status.NEGOTIATION: 'badge-amber',
            Lead.Status.WON: 'badge-green',
            Lead.Status.LOST: 'badge-red',
        }
        color = colors.get(obj.status, 'badge-gray')
        return format_html('<span class="badge-pill {}">{}</span>', color, obj.get_status_display())

    @admin.display(description='Priority', ordering='priority')
    def priority_badge(self, obj):
        colors = {
            Lead.Priority.HIGH: 'badge-red',
            Lead.Priority.MEDIUM: 'badge-amber',
            Lead.Priority.LOW: 'badge-gray',
        }
        color = colors.get(obj.priority, 'badge-gray')
        return format_html('<span class="badge-pill {}">{}</span>', color, obj.get_priority_display())

    @admin.display(description='Est. Value', ordering='estimated_value')
    def formatted_value(self, obj):
        formatted = f"${float(obj.estimated_value or 0):,.0f}"
        return format_html('<span class="metric-highlight">{}</span>', formatted)

    @admin.action(description="Advance selected leads to QUALIFIED")
    def advance_to_qualified(self, request, queryset):
        updated = queryset.update(status=Lead.Status.QUALIFIED)
        self.message_user(request, f"{updated} lead(s) advanced to Qualified.")

    @admin.action(description="Advance selected leads to PROPOSAL")
    def advance_to_proposal(self, request, queryset):
        updated = queryset.update(status=Lead.Status.PROPOSAL)
        self.message_user(request, f"{updated} lead(s) advanced to Proposal.")

    @admin.action(description="Mark selected leads as WON")
    def mark_as_won(self, request, queryset):
        updated = queryset.update(status=Lead.Status.WON)
        self.message_user(request, f"{updated} lead(s) marked as Won.")

    @admin.action(description="Mark selected leads as LOST")
    def mark_as_lost(self, request, queryset):
        updated = queryset.update(status=Lead.Status.LOST)
        self.message_user(request, f"{updated} lead(s) marked as Lost.")
