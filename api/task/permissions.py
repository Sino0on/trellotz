from rest_framework import permissions
from django.conf import settings
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from apps.task.models import Board, Task


class CanChangeTask(permissions.BasePermission):
    message = _('Недостаточно прав')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ['POST', 'PUT']:
                board = get_object_or_404(Board, id=request.data.get('board'))
                if request.user in board.admins.all():
                    return True
                return False
            return True
        return False


class IsAssignee(permissions.BasePermission):
    message = _("Недостаточно прав")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method == 'GET':
                if request.user == get_object_or_404(Task, id=view.kwargs.get('pk')).assignee:
                    return True
                return False