from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        MANAGER = 'MANAGER', 'Manager'
        SALES_REP = 'SALES_REP', 'Sales Representative'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SALES_REP,
        help_text="Designates the user's operational role within the CRM."
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def is_manager(self):
        return self.role == self.Role.MANAGER or self.is_admin()

    def is_sales_rep(self):
        return self.role == self.Role.SALES_REP

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
