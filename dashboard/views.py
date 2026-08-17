import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone

from customers.models import Customer
from leads.models import Lead
from opportunities.models import Opportunity
from tasks.models import Task


@login_required
def dashboard_view(request):
    # Aggregated KPI Metrics
    total_customers = Customer.objects.count()
    total_leads = Lead.objects.count()
    open_opportunities = Opportunity.objects.exclude(stage__in=[Opportunity.Stage.CLOSED_WON, Opportunity.Stage.CLOSED_LOST]).count()
    won_opportunities = Opportunity.objects.filter(stage=Opportunity.Stage.CLOSED_WON).count()
    
    total_sales_value = Opportunity.objects.filter(stage=Opportunity.Stage.CLOSED_WON).aggregate(total=Sum('amount'))['total'] or 0.00
    pipeline_sales_value = Opportunity.objects.exclude(stage=Opportunity.Stage.CLOSED_LOST).aggregate(total=Sum('amount'))['total'] or 0.00
    
    pending_tasks = Task.objects.filter(status__in=[Task.Status.PENDING, Task.Status.IN_PROGRESS]).count()
    overdue_tasks = Task.objects.filter(due_date__lt=timezone.now(), status__in=[Task.Status.PENDING, Task.Status.IN_PROGRESS]).count()

    # Chart 1 Data: Lead Stage Breakdown
    lead_stages = Lead.Status.choices
    lead_stage_labels = [label for code, label in lead_stages]
    lead_counts_dict = dict(Lead.objects.values('status').annotate(count=Count('id')).values_list('status', 'count'))
    lead_stage_data = [lead_counts_dict.get(code, 0) for code, label in lead_stages]

    # Chart 2 Data: Opportunity Pipeline Values by Stage
    op_stages = Opportunity.Stage.choices
    op_stage_labels = [label for code, label in op_stages]
    op_values_dict = dict(Opportunity.objects.values('stage').annotate(total=Sum('amount')).values_list('stage', 'total'))
    op_stage_data = [float(op_values_dict.get(code, 0.0) or 0.0) for code, label in op_stages]

    # Feeds: Recent Activities
    recent_customers = Customer.objects.select_related('assigned_to').order_by('-created_at')[:5]
    recent_leads = Lead.objects.select_related('assigned_to').order_by('-created_at')[:5]
    recent_tasks = Task.objects.select_related('assigned_to').order_by('due_date')[:5]

    context = {
        # KPIs
        'total_customers': total_customers,
        'total_leads': total_leads,
        'open_opportunities': open_opportunities,
        'won_opportunities': won_opportunities,
        'total_sales_value': total_sales_value,
        'pipeline_sales_value': pipeline_sales_value,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,

        # Chart JSON
        'lead_stage_labels_json': json.dumps(lead_stage_labels),
        'lead_stage_data_json': json.dumps(lead_stage_data),
        'op_stage_labels_json': json.dumps(op_stage_labels),
        'op_stage_data_json': json.dumps(op_stage_data),

        # Feeds
        'recent_customers': recent_customers,
        'recent_leads': recent_leads,
        'recent_tasks': recent_tasks,
    }
    return render(request, 'dashboard/dashboard.html', context)
