from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.task.views import BoardViewSet, TaskViewSet,\
    TaskHistoryViewSet, StatusViewSet, TaskChangeView


router = DefaultRouter()
router.register(r'boards', BoardViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'taskhistory', TaskHistoryViewSet)
router.register(r'status', StatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('change_status/<int:pk>', TaskChangeView.as_view())
]
