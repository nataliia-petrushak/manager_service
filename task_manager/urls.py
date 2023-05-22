from django.urls import path

from .views import (
    index,
    TaskTypeListView,
    TaskTypeCreate,
    TaskTypeUpdate,
    TaskTypeDelete,
    PositionListView,
    PositionCreate,
    PositionUpdate,
    PositionDelete,
    ProjectDetailView,
    ProjectCreate,
    ProjectUpdate,
    ProjectDelete,
    TeamDetailView,
    WorkerDetailView,
    WorkerCreate,
    WorkerUpdate,
    WorkerDelete,
    TaskDetailView,
    TaskCreate,
    TaskUpdate,
    TaskDelete,
    TeamCreate,
    TeamUpdate,
    TeamDelete,
    toggle_assign_to_task,
    toggle_assign_to_project,
    toggle_add_to_team,
    dashboard,
    tasks_of_project_by_tags,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "task-types/",
        TaskTypeListView.as_view(),
        name="task-type-list"
    ),
    path(
        "task-types/create/",
        TaskTypeCreate.as_view(),
        name="task-type-create"
    ),
    path(
        "task-types/<int:pk>/update/",
        TaskTypeUpdate.as_view(),
        name="task-type-update"
    ),
    path(
        "task-types/<int:pk>/delete/",
        TaskTypeDelete.as_view(),
        name="task-type-delete"
    ),
    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list"
    ),
    path(
        "positions/create/",
        PositionCreate.as_view(),
        name="position-create"
    ),
    path(
        "positions/<int:pk>/update/",
        PositionUpdate.as_view(),
        name="position-update"
    ),
    path(
        "positions/<int:pk>/delete/",
        PositionDelete.as_view(),
        name="position-delete"
    ),
    path(
        "teams/<int:pk>/",
        TeamDetailView.as_view(),
        name="team-detail"
    ),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "accounts/register/",
        WorkerCreate.as_view(),
        name="worker-create"
    ),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdate.as_view(),
        name="worker-update"
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerDelete.as_view(),
        name="worker-delete"
    ),
    path(
        "project/<int:pk>/",
        tasks_of_project_by_tags,
        name="project-tasks"
    ),
    path(
        "project/<int:pk>/<slug:slug>/",
        tasks_of_project_by_tags,
        name="tagged"
        ),
    path(
        "tasks/<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "tasks/create/",
        TaskCreate.as_view(),
        name="task-create"
    ),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdate.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDelete.as_view(),
        name="task-delete"
    ),
    path(
        "tasks/<int:pk>/toggle-assign/",
        toggle_assign_to_task,
        name="toggle-task-assign",
    ),
    path(
        "dashboard/",
        dashboard,
        name="dashboard"
    ),
    path(
        "projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail"
    ),
    path(
        "projects/<int:pk>/toggle-assign/",
        toggle_assign_to_project,
        name="toggle-project-assign",
    ),
    path(
        "projects/create/",
        ProjectCreate.as_view(),
        name="project-create"
        ),
    path(
        "projects/<int:pk>/update",
        ProjectUpdate.as_view(),
        name="project-update"
        ),
    path(
        "projects/<int:pk>/delete",
        ProjectDelete.as_view(),
        name="project-delete"
        ),
    path(
        "teams/create/",
        TeamCreate.as_view(),
        name="team-create"
    ),
    path(
        "teams/<int:pk>/update/",
        TeamUpdate.as_view(),
        name="team-update"
    ),
    path("teams/<int:pk>/delete",
         TeamDelete.as_view(),
         name="team-delete"),
    path(
        "teams/<int:pk>/toggle-add/",
        toggle_add_to_team,
        name="toggle-team-add",
    ),
]

app_name = "task_manager"
