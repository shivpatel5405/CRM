from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'task_type_badge',
        'priority_badge',
        'status_badge',
        'due_date_display',
        'related_entity',
        'assigned_to'
    )
    list_filter = ('status', 'priority', 'task_type', 'assigned_to', 'due_date')
    search_fields = ('title', 'description', 'customer__name', 'lead__title', 'opportunity__name')
    date_hierarchy = 'due_date'
    autocomplete_fields = ('assigned_to', 'customer', 'lead', 'opportunity')
    actions = ('mark_as_completed', 'mark_as_in_progress', 'mark_as_pending')

    @admin.display(description='Type', ordering='task_type')
    def task_type_badge(self, obj):
        icons = {
            Task.TaskType.CALL: '📞 Call',
            Task.TaskType.MEETING: '👥 Meeting',
            Task.TaskType.FOLLOW_UP: '🔄 Follow-up',
            Task.TaskType.TASK: '✅ Task',
        }
        text = icons.get(obj.task_type, obj.get_task_type_display())
        return format_html('<span class="badge-pill badge-gray">{}</span>', text)

    @admin.display(description='Priority', ordering='priority')
    def priority_badge(self, obj):
        colors = {
            Task.Priority.HIGH: 'badge-red',
            Task.Priority.MEDIUM: 'badge-amber',
            Task.Priority.LOW: 'badge-gray',
        }
        color = colors.get(obj.priority, 'badge-gray')
        return format_html('<span class="badge-pill {}">{}</span>', color, obj.get_priority_display())

    @admin.display(description='Status', ordering='status')
    def status_badge(self, obj):
        colors = {
            Task.Status.COMPLETED: 'badge-green',
            Task.Status.IN_PROGRESS: 'badge-blue',
            Task.Status.PENDING: 'badge-amber',
            Task.Status.CANCELLED: 'badge-gray',
        }
        color = colors.get(obj.status, 'badge-gray')
        return format_html('<span class="badge-pill {}">{}</span>', color, obj.get_status_display())

    @admin.display(description='Due Date', ordering='due_date')
    def due_date_display(self, obj):
        if not obj.due_date:
            return "—"
        
        formatted = obj.due_date.strftime("%b %d, %Y %H:%M")
        if obj.is_overdue:
            return format_html('<span style="color: #ef4444; font-weight: 700;">🚨 OVERDUE ({})</span>', formatted)
        return formatted

    @admin.display(description='Related Entity')
    def related_entity(self, obj):
        if obj.customer:
            return format_html('🏢 Customer: <strong>{}</strong>', obj.customer.name)
        elif obj.lead:
            return format_html('🎯 Lead: <strong>{}</strong>', obj.lead.title)
        elif obj.opportunity:
            return format_html('💼 Deal: <strong>{}</strong>', obj.opportunity.name)
        return "—"

    @admin.action(description="Mark selected tasks as COMPLETED")
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status=Task.Status.COMPLETED)
        self.message_user(request, f"{updated} task(s) marked as Completed.")

    @admin.action(description="Mark selected tasks as IN PROGRESS")
    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status=Task.Status.IN_PROGRESS)
        self.message_user(request, f"{updated} task(s) marked as In Progress.")

    @admin.action(description="Mark selected tasks as PENDING")
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status=Task.Status.PENDING)
        self.message_user(request, f"{updated} task(s) marked as Pending.")
