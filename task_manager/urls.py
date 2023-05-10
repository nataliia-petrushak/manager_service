from django.urls import path

from .views import (
    index,
    TaskTypeListView,
    TaskTypeCreate,
    TaskTypeUpdate,
    TaskTypeDelete,
    PositionListView,
    WorkerListView,
    TaskListView,
    TaskDetailView,
    TaskCreate,
    TaskUpdate,
    TaskDelete,
    WorkerDetailView
)

urlpatterns = [
    path("", index, name="index"),
    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task-types/create/", TaskTypeCreate.as_view(), name="task-type-create"),
    path("task-types/<int:pk>/update/", TaskTypeUpdate.as_view(), name="task-type-update"),
    path("task-types/<int:pk>/delete/", TaskTypeDelete.as_view(), name="task-type-delete"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreate.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdate.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDelete.as_view(), name="task-delete"),
]

app_name = "task_manager"
