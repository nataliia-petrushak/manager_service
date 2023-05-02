from django.urls import path

from .views import index, WorkerListView

urlpatterns = [
    path("", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list")
]

app_name = "task_manager"
