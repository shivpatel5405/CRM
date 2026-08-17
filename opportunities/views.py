from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from .models import Opportunity
from .forms import OpportunityForm


@login_required
def opportunity_list_view(request):
    queryset = Opportunity.objects.select_related('customer', 'assigned_to').all()

    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(customer__name__icontains=query)
        )

    stage_filter = request.GET.get('stage', '').strip()
    if stage_filter:
        queryset = queryset.filter(stage=stage_filter)

    # Aggregated metrics
    total_pipeline_value = queryset.aggregate(total=Sum('amount'))['total'] or 0.00
    won_value = queryset.filter(stage=Opportunity.Stage.CLOSED_WON).aggregate(total=Sum('amount'))['total'] or 0.00

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'stage_filter': stage_filter,
        'stage_choices': Opportunity.Stage.choices,
        'total_pipeline_value': total_pipeline_value,
        'won_value': won_value,
    }
    return render(request, 'opportunities/opportunity_list.html', context)


@login_required
def opportunity_detail_view(request, pk):
    opportunity = get_object_or_404(Opportunity.objects.select_related('customer', 'assigned_to'), pk=pk)
    tasks = opportunity.tasks.all()
    notes = opportunity.crm_notes.select_related('author').all()
    return render(request, 'opportunities/opportunity_detail.html', {
        'opportunity': opportunity,
        'tasks': tasks,
        'notes': notes,
    })


@login_required
def opportunity_create_view(request):
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            if not opportunity.assigned_to:
                opportunity.assigned_to = request.user
            opportunity.save()
            messages.success(request, f"Opportunity '{opportunity.name}' created successfully!")
            return redirect('opportunity-detail', pk=opportunity.pk)
    else:
        form = OpportunityForm(initial={'assigned_to': request.user})

    return render(request, 'opportunities/opportunity_form.html', {'form': form, 'title': 'Create Opportunity'})


@login_required
def opportunity_update_view(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    if request.method == 'POST':
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            messages.success(request, f"Opportunity '{opportunity.name}' updated successfully!")
            return redirect('opportunity-detail', pk=opportunity.pk)
    else:
        form = OpportunityForm(instance=opportunity)

    return render(request, 'opportunities/opportunity_form.html', {'form': form, 'title': f'Edit Opportunity: {opportunity.name}'})


@login_required
def opportunity_delete_view(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    if request.method == 'POST':
        name = opportunity.name
        opportunity.delete()
        messages.success(request, f"Opportunity '{name}' deleted.")
        return redirect('opportunity-list')

    return render(request, 'opportunities/opportunity_confirm_delete.html', {'opportunity': opportunity})
