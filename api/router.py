from django.urls import path, include


urlpatterns = [
    path("task/", include("api.task.urls")),
    path("docs/", include("api.openapi.urls")),
]
