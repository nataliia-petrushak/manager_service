from django.urls import path

from .views import (
    index,
    WorkerListView,
    TaskListView,
    WorkerDetailView
)

urlpatterns = [
    path("", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("tasks/", TaskListView.as_view(), name="task-list")
]

app_name = "task_manager"
