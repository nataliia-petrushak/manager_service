from django.urls import path

from .views import (
    index,
    TaskTypeListView,
    PositionListView,
    WorkerListView,
    TaskListView,
    TaskDetailView,
    WorkerDetailView
)

urlpatterns = [
    path("", index, name="index"),
    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail")
]

app_name = "task_manager"
