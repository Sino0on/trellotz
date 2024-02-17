from django.contrib import admin
from apps.task.models import Task, TaskHistory, Status, Board


admin.site.register(Task)
admin.site.register(TaskHistory)
admin.site.register(Status)
admin.site.register(Board)
