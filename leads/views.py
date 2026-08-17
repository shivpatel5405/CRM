from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction
from .models import Lead
from .forms import LeadForm
from customers.models import Customer, Contact


@login_required
def lead_list_view(request):
    queryset = Lead.objects.select_related('assigned_to').all()

    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(company__icontains=query) |
            Q(email__icontains=query)
        )

    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    priority_filter = request.GET.get('priority', '').strip()
    if priority_filter:
        queryset = queryset.filter(priority=priority_filter)

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'status_choices': Lead.Status.choices,
        'priority_choices': Lead.Priority.choices,
    }
    return render(request, 'leads/lead_list.html', context)


@login_required
def lead_pipeline_view(request):
    """Kanban Pipeline View displaying leads by stage."""
    leads = Lead.objects.select_related('assigned_to').all()
    pipeline = {}
    for stage_code, stage_label in Lead.Status.choices:
        pipeline[stage_code] = {
            'label': stage_label,
            'leads': [l for l in leads if l.status == stage_code]
        }

    return render(request, 'leads/lead_pipeline.html', {'pipeline': pipeline})


@login_required
def lead_detail_view(request, pk):
    lead = get_object_or_404(Lead.objects.select_related('assigned_to'), pk=pk)
    return render(request, 'leads/lead_detail.html', {'lead': lead})


@login_required
def lead_create_view(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            if not lead.assigned_to:
                lead.assigned_to = request.user
            lead.save()
            messages.success(request, f"Lead '{lead.title}' created successfully!")
            return redirect('lead-detail', pk=lead.pk)
    else:
        form = LeadForm(initial={'assigned_to': request.user})

    return render(request, 'leads/lead_form.html', {'form': form, 'title': 'Create New Lead'})


@login_required
def lead_update_view(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, f"Lead '{lead.title}' updated successfully!")
            return redirect('lead-detail', pk=lead.pk)
    else:
        form = LeadForm(instance=lead)

    return render(request, 'leads/lead_form.html', {'form': form, 'title': f'Edit Lead: {lead.title}'})


@login_required
def lead_delete_view(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        title = lead.title
        lead.delete()
        messages.success(request, f"Lead '{title}' was deleted.")
        return redirect('lead-list')

    return render(request, 'leads/lead_confirm_delete.html', {'lead': lead})


@login_required
def convert_lead_to_customer_view(request, pk):
    """Business Logic: Convert a Lead into an Active Customer record."""
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == 'POST':
        with transaction.atomic():
            # Check if customer already exists with this email
            customer, created = Customer.objects.get_or_create(
                email=lead.email,
                defaults={
                    'name': lead.company or f"{lead.first_name} {lead.last_name}",
                    'company': lead.company,
                    'phone': lead.phone,
                    'status': Customer.Status.ACTIVE,
                    'assigned_to': lead.assigned_to or request.user,
                }
            )

            # Create primary contact for the customer
            Contact.objects.get_or_create(
                customer=customer,
                email=lead.email,
                defaults={
                    'first_name': lead.first_name,
                    'last_name': lead.last_name,
                    'phone': lead.phone,
                    'is_primary': True
                }
            )

            # Update lead status to WON
            lead.status = Lead.Status.WON
            lead.save()

            if created:
                messages.success(request, f"Lead converted successfully! New customer '{customer.name}' created.")
            else:
                messages.info(request, f"Lead converted! Linked to existing customer '{customer.name}'.")

            return redirect('customer-detail', pk=customer.pk)

    return render(request, 'leads/lead_convert_confirm.html', {'lead': lead})
