from rest_framework import serializers
from accounts.models import User
from customers.models import Customer, Contact, Note
from leads.models import Lead
from opportunities.models import Opportunity
from tasks.models import Task


class UserSerializer(serializers.ModelResourceSerializer if hasattr(serializers, 'ModelResourceSerializer') else serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'customer', 'first_name', 'last_name', 'email', 'phone', 'designation', 'is_primary', 'created_at')


class CustomerSerializer(serializers.ModelSerializer):
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = (
            'id', 'name', 'email', 'phone', 'company',
            'address', 'status', 'assigned_to', 'assigned_to_detail',
            'contacts', 'created_at', 'updated_at'
        )


class LeadSerializer(serializers.ModelSerializer):
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)

    class Meta:
        model = Lead
        fields = (
            'id', 'title', 'first_name', 'last_name', 'company',
            'email', 'phone', 'source', 'status', 'priority',
            'estimated_value', 'assigned_to', 'assigned_to_detail',
            'follow_up_date', 'notes', 'created_at', 'updated_at'
        )


class OpportunitySerializer(serializers.ModelSerializer):
    customer_detail = CustomerSerializer(source='customer', read_only=True)
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)

    class Meta:
        model = Opportunity
        fields = (
            'id', 'name', 'customer', 'customer_detail', 'amount',
            'stage', 'probability', 'expected_closing_date',
            'assigned_to', 'assigned_to_detail', 'notes',
            'created_at', 'updated_at'
        )


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)
    is_overdue = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'task_type', 'priority',
            'status', 'due_date', 'is_overdue', 'assigned_to',
            'assigned_to_detail', 'customer', 'lead', 'opportunity',
            'created_at', 'updated_at'
        )
