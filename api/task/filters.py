import django_filters
from apps.task.models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.NumberFilter(field_name="status__id")
    status_order = django_filters.NumberFilter(field_name="status__order")
    created_at = django_filters.DateFromToRangeFilter()
    assignee = django_filters.NumberFilter(field_name="assignee__id")

    class Meta:
        model = Task
        fields = ['status', 'status_order', 'created_at', 'assignee']
