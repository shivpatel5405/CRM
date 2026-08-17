from rest_framework import viewsets, permissions, filters
from accounts.models import User
from customers.models import Customer
from leads.models import Lead
from opportunities.models import Opportunity
from tasks.models import Task

from .serializers import (
    UserSerializer,
    CustomerSerializer,
    LeadSerializer,
    OpportunitySerializer,
    TaskSerializer
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint to view user profiles."""
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']


class CustomerViewSet(viewsets.ModelViewSet):
    """API endpoint for Customer CRUD operations."""
    queryset = Customer.objects.select_related('assigned_to').prefetch_related('contacts').all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email', 'company', 'phone']


class LeadViewSet(viewsets.ModelViewSet):
    """API endpoint for Lead CRUD operations."""
    queryset = Lead.objects.select_related('assigned_to').all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'first_name', 'last_name', 'company', 'email']


class OpportunityViewSet(viewsets.ModelViewSet):
    """API endpoint for Sales Opportunities CRUD operations."""
    queryset = Opportunity.objects.select_related('customer', 'assigned_to').all()
    serializer_class = OpportunitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'customer__name']


class TaskViewSet(viewsets.ModelViewSet):
    """API endpoint for Task and Activity CRUD operations."""
    queryset = Task.objects.select_related('assigned_to', 'customer', 'lead', 'opportunity').all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
