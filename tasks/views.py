from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Task
from .forms import TaskForm


@login_required
def task_list_view(request):
    queryset = Task.objects.select_related('assigned_to', 'customer', 'lead', 'opportunity').all()

    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    status_filter = request.GET.get('status', '').strip()
    if status_filter == 'OVERDUE':
        queryset = queryset.filter(due_date__lt=timezone.now(), status__in=[Task.Status.PENDING, Task.Status.IN_PROGRESS])
    elif status_filter:
        queryset = queryset.filter(status=status_filter)

    priority_filter = request.GET.get('priority', '').strip()
    if priority_filter:
        queryset = queryset.filter(priority=priority_filter)

    type_filter = request.GET.get('task_type', '').strip()
    if type_filter:
        queryset = queryset.filter(task_type=type_filter)

    overdue_count = Task.objects.filter(due_date__lt=timezone.now(), status__in=[Task.Status.PENDING, Task.Status.IN_PROGRESS]).count()

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'type_filter': type_filter,
        'status_choices': Task.Status.choices,
        'priority_choices': Task.Priority.choices,
        'type_choices': Task.TaskType.choices,
        'overdue_count': overdue_count,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_detail_view(request, pk):
    task = get_object_or_404(Task.objects.select_related('assigned_to', 'customer', 'lead', 'opportunity'), pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_create_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if not task.assigned_to:
                task.assigned_to = request.user
            task.save()
            messages.success(request, f"Task '{task.title}' created successfully!")
            return redirect('task-list')
    else:
        form = TaskForm(initial={'assigned_to': request.user, 'due_date': timezone.now() + timezone.timedelta(days=1)})

    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create New Task'})


@login_required
def task_update_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f"Task '{task.title}' updated successfully!")
            return redirect('task-list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {'form': form, 'title': f'Edit Task: {task.title}'})


@login_required
def task_delete_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f"Task '{title}' deleted.")
        return redirect('task-list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def toggle_task_status_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.status == Task.Status.COMPLETED:
        task.status = Task.Status.PENDING
        messages.info(request, f"Task '{task.title}' marked as Pending.")
    else:
        task.status = Task.Status.COMPLETED
        messages.success(request, f"Task '{task.title}' marked as Completed!")
    task.save()
    return redirect('task-list')
