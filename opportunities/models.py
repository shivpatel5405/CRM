from django.conf import settings
from django.db import models
from customers.models import Customer


class Opportunity(models.Model):
    class Stage(models.TextChoices):
        QUALIFICATION = 'QUALIFICATION', 'Qualification'
        NEEDS_ANALYSIS = 'NEEDS_ANALYSIS', 'Needs Analysis'
        PROPOSAL = 'PROPOSAL', 'Proposal / Price Quote'
        NEGOTIATION = 'NEGOTIATION', 'Negotiation / Review'
        CLOSED_WON = 'CLOSED_WON', 'Closed Won'
        CLOSED_LOST = 'CLOSED_LOST', 'Closed Lost'

    name = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='opportunities'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    stage = models.CharField(
        max_length=30,
        choices=Stage.choices,
        default=Stage.QUALIFICATION
    )
    probability = models.PositiveIntegerField(
        default=50,
        help_text="Estimated win probability percentage (0-100)"
    )
    expected_closing_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='opportunities'
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Opportunities"

    def __str__(self):
        return f"{self.name} - ${self.amount:,.2f} ({self.get_stage_display()})"
