from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Board(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    people = models.ManyToManyField(User, related_name='boards')
    admins = models.ManyToManyField(User, related_name='admin_boards')

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='statuses', db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('board', 'order')


class TaskHistory(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} - {self.status.name} - {self.changed_at}"


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    board = models.ForeignKey(Board, related_name='tasks', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, related_name='tasks', on_delete=models.CASCADE, db_index=True)
    creator = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)
    assignee = models.ForeignKey(
        User,
        related_name='assigned_tasks',
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.status.board != self.board:
            print('sad')
            return False
        data = super().save(force_insert, force_update, using, update_fields)
        TaskHistory.objects.create(task=self, status=self.status)
        return data

    def can_change_status(self, new_status):
        current_status_order = self.status.order
        new_status_order = new_status.order
        if new_status_order != current_status_order:
            print('da')
            return new_status_order == current_status_order + 1 or new_status_order == current_status_order - 1
        return True
    # def change_task_status(self, new_status):
    #     if self.can_change_status(new_status):
    #         self.status = new_status
    #         self.save()
    #         return True
    #     else:
    #         return False
