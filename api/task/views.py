from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.views import APIView

from apps.task.models import Board, Task, TaskHistory, Status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.task.serializers import BoardSerializer, TaskSerializer,\
    StatusSerializer, TaskHistorySerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from api.task.permissions import CanChangeTask, IsAssignee
from api.task.serializers import TaskSerializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from api.task.filters import TaskFilter
from api.task.tasks import send_status_change_email


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    # permission_classes = [IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [CanChangeTask]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TaskFilter

    def update(self, request, *args, **kwargs):
        print(request.data)
        task = Task.objects.get(id=kwargs['pk'])
        if task.can_change_status(get_object_or_404(Status, id=request.data.get('status'))):
            if task.status.id != request.data.get('status'):
                send_status_change_email(task, task.status__id, request.data.get('status'), task.assignee.email)
            return super().update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data)
        if not data.is_valid():
            return Response(data=data.errors, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        task = data.save(creator=user)
        task.save()
        task = Task.objects.get(id=task.pk)
        data = TaskSerializer(instance=task).data
        return Response(data, status=status.HTTP_200_OK)


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.pk in get_object_or_404(Board, id=request.data['board']).admins.all():
            return super().create(request, *args, **kwargs)
        return Response(data={"Error": "У вас нет прав на создание"}, status=status.HTTP_400_BAD_REQUEST)


class TaskHistoryViewSet(viewsets.ModelViewSet):
    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistorySerializer
    # permission_classes = [IsAuthenticated]


@extend_schema_view(
    get=extend_schema(
        description='URL для изменения статуса по приоритету',
        summary='URL для изменения статуса',
        parameters=[
            OpenApiParameter(name='status',
                             description='Статус',
                             type=OpenApiTypes.INT, required=True),
        ]
    ),
)
class TaskChangeView(APIView):
    permission_classes = (IsAssignee,)

    def get(self, request, *args, **kwargs):
        status1 = request.query_params.get('status')
        task = get_object_or_404(Task, id=kwargs['pk'])
        status2 = get_object_or_404(Status, id=status1)
        if task.can_change_status(status2):
            if task.status.id != int(status1):
                send_status_change_email(task, task.status.id, request.query_params.get('status'), task.assignee.email)
                task.status = status2
                task.save()
                return Response(TaskSerializer(instance=task).data, status=status.HTTP_200_OK)
            return Response(data={"Error": "Статус тот же"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
