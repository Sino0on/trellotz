from rest_framework import serializers
from apps.task.models import Board, Task, Status, TaskHistory
from api.auth.serializers import UserShortSerializer


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    creator = UserShortSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskHistory
        fields = '__all__'
