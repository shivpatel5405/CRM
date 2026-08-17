from django.conf import settings
from django.db import models
from django.utils import timezone
from customers.models import Customer
from leads.models import Lead
from opportunities.models import Opportunity


class Task(models.Model):
    class TaskType(models.TextChoices):
        TASK = 'TASK', 'Task'
        CALL = 'CALL', 'Phone Call'
        MEETING = 'MEETING', 'Meeting'
        FOLLOW_UP = 'FOLLOW_UP', 'Follow-up'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    task_type = models.CharField(
        max_length=20,
        choices=TaskType.choices,
        default=TaskType.TASK
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    due_date = models.DateTimeField()
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tasks'
    )
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tasks'
    )
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"[{self.get_task_type_display()}] {self.title} - {self.get_status_display()}"

    @property
    def is_overdue(self):
        return self.due_date < timezone.now() and self.status in [self.Status.PENDING, self.Status.IN_PROGRESS]
