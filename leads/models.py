from django.conf import settings
from django.db import models


class Lead(models.Model):
    class Source(models.TextChoices):
        WEBSITE = 'WEBSITE', 'Website'
        REFERRAL = 'REFERRAL', 'Referral'
        COLD_CALL = 'COLD_CALL', 'Cold Call'
        LINKEDIN = 'LINKEDIN', 'LinkedIn'
        EVENT = 'EVENT', 'Event / Conference'
        OTHER = 'OTHER', 'Other'

    class Status(models.TextChoices):
        NEW = 'NEW', 'New'
        CONTACTED = 'CONTACTED', 'Contacted'
        QUALIFIED = 'QUALIFIED', 'Qualified'
        PROPOSAL = 'PROPOSAL', 'Proposal'
        NEGOTIATION = 'NEGOTIATION', 'Negotiation'
        WON = 'WON', 'Won'
        LOST = 'LOST', 'Lost'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    title = models.CharField(max_length=255, help_text="Short title describing the lead opportunity")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    source = models.CharField(
        max_length=20,
        choices=Source.choices,
        default=Source.WEBSITE
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    estimated_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads'
    )
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.company or self.first_name} ({self.get_status_display()})"
