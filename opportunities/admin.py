from django.contrib import admin
from .models import Opportunity


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer', 'amount', 'stage', 'probability', 'expected_closing_date', 'assigned_to')
    list_filter = ('stage', 'assigned_to', 'expected_closing_date')
    search_fields = ('name', 'customer__name')
