from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Opportunity


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'customer',
        'formatted_amount',
        'stage_badge',
        'probability_display',
        'weighted_value',
        'closing_date_display',
        'assigned_to'
    )
    list_filter = ('stage', 'assigned_to', 'expected_closing_date', 'created_at')
    search_fields = ('name', 'customer__name', 'notes')
    date_hierarchy = 'expected_closing_date'
    autocomplete_fields = ('customer', 'assigned_to')
    actions = ('mark_as_won', 'mark_as_lost')

    @admin.display(description='Deal Value', ordering='amount')
    def formatted_amount(self, obj):
        formatted = f"${float(obj.amount or 0):,.0f}"
        return format_html('<span class="metric-highlight">{}</span>', formatted)

    @admin.display(description='Stage', ordering='stage')
    def stage_badge(self, obj):
        colors = {
            Opportunity.Stage.QUALIFICATION: 'badge-cyan',
            Opportunity.Stage.NEEDS_ANALYSIS: 'badge-blue',
            Opportunity.Stage.PROPOSAL: 'badge-purple',
            Opportunity.Stage.NEGOTIATION: 'badge-amber',
            Opportunity.Stage.CLOSED_WON: 'badge-green',
            Opportunity.Stage.CLOSED_LOST: 'badge-red',
        }
        color = colors.get(obj.stage, 'badge-gray')
        return format_html('<span class="badge-pill {}">{}</span>', color, obj.get_stage_display())

    @admin.display(description='Win Probability', ordering='probability')
    def probability_display(self, obj):
        return format_html(
            '<div style="min-width: 90px;">'
            '<span style="font-weight: 700; font-size: 0.75rem;">{}%</span>'
            '<div style="background: #e2e8f0; border-radius: 4px; height: 6px; overflow: hidden; margin-top: 3px;">'
            '<div style="background: #4f46e5; height: 100%; width: {}%;"></div>'
            '</div>'
            '</div>',
            obj.probability,
            min(obj.probability, 100)
        )

    @admin.display(description='Weighted Value')
    def weighted_value(self, obj):
        val = float(obj.amount or 0) * (float(obj.probability or 0) / 100.0)
        formatted = f"${val:,.0f}"
        return format_html('<span>{}</span>', formatted)

    @admin.display(description='Expected Close', ordering='expected_closing_date')
    def closing_date_display(self, obj):
        if not obj.expected_closing_date:
            return "—"
        
        is_past = (
            obj.expected_closing_date < timezone.now().date() and
            obj.stage not in [Opportunity.Stage.CLOSED_WON, Opportunity.Stage.CLOSED_LOST]
        )
        if is_past:
            return format_html('<span style="color: #ef4444; font-weight: 600;">⚠️ {}</span>', obj.expected_closing_date.strftime("%b %d, %Y"))
        return obj.expected_closing_date.strftime("%b %d, %Y")

    @admin.action(description="Mark selected opportunities as CLOSED WON")
    def mark_as_won(self, request, queryset):
        updated = queryset.update(stage=Opportunity.Stage.CLOSED_WON, probability=100)
        self.message_user(request, f"{updated} opportunity(s) marked as Closed Won.")

    @admin.action(description="Mark selected opportunities as CLOSED LOST")
    def mark_as_lost(self, request, queryset):
        updated = queryset.update(stage=Opportunity.Stage.CLOSED_LOST, probability=0)
        self.message_user(request, f"{updated} opportunity(s) marked as Closed Lost.")
