from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin


def admin_required(function=None):
    """Decorator for views that checks if the user is an Admin or Superuser."""
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and (u.is_admin() or u.is_superuser),
        login_url='login'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def manager_required(function=None):
    """Decorator for views that checks if the user is a Manager or Admin."""
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and (u.is_manager() or u.is_admin() or u.is_superuser),
        login_url='login'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


class RoleRequiredMixin(UserPassesTestMixin):
    """CBV Mixin to restrict access based on allowed roles."""
    allowed_roles = []

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        if self.request.user.is_superuser:
            return True
        return self.request.user.role in self.allowed_roles
