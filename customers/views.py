from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Customer, Contact, Note
from .forms import CustomerForm, ContactForm, NoteForm


@login_required
def customer_list_view(request):
    queryset = Customer.objects.select_related('assigned_to').all()

    # Search query
    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(company__icontains=query) |
            Q(phone__icontains=query)
        )

    # Status filter
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    # Assigned to filter
    assigned_filter = request.GET.get('assigned_to', '').strip()
    if assigned_filter:
        queryset = queryset.filter(assigned_to_id=assigned_filter)

    # Pagination
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'assigned_filter': assigned_filter,
        'status_choices': Customer.Status.choices,
    }
    return render(request, 'customers/customer_list.html', context)


@login_required
def customer_detail_view(request, pk):
    customer = get_object_or_404(Customer.objects.select_related('assigned_to'), pk=pk)
    contacts = customer.contacts.all()
    notes = customer.crm_notes.select_related('author').all()
    opportunities = customer.opportunities.all()
    tasks = customer.tasks.all()

    contact_form = ContactForm()
    note_form = NoteForm()

    context = {
        'customer': customer,
        'contacts': contacts,
        'notes': notes,
        'opportunities': opportunities,
        'tasks': tasks,
        'contact_form': contact_form,
        'note_form': note_form,
    }
    return render(request, 'customers/customer_detail.html', context)


@login_required
def customer_create_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            if not customer.assigned_to:
                customer.assigned_to = request.user
            customer.save()
            messages.success(request, f"Customer '{customer.name}' created successfully!")
            return redirect('customer-detail', pk=customer.pk)
    else:
        form = CustomerForm(initial={'assigned_to': request.user})

    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Create Customer'})


@login_required
def customer_update_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f"Customer '{customer.name}' updated successfully!")
            return redirect('customer-detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/customer_form.html', {'form': form, 'title': f'Edit Customer: {customer.name}'})


@login_required
def customer_delete_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        name = customer.name
        customer.delete()
        messages.success(request, f"Customer '{name}' was deleted.")
        return redirect('customer-list')

    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})


@login_required
def add_contact_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.customer = customer
            contact.save()
            messages.success(request, f"Contact '{contact.first_name} {contact.last_name}' added to {customer.name}.")
        else:
            messages.error(request, "Failed to add contact. Please check form inputs.")
    return redirect('customer-detail', pk=customer.pk)


@login_required
def add_note_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.customer = customer
            note.author = request.user
            note.save()
            messages.success(request, "Note added successfully!")
        else:
            messages.error(request, "Note content cannot be empty.")
    return redirect('customer-detail', pk=customer.pk)
