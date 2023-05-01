from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import generic

from .models import Task, TaskType, Position


def index(request):
    """View function for the home page of the site."""

    context = {
        "num_tasks": Task.objects.count(),
        "num_task_types": TaskType.objects.count(),
        "num_positions": Position.objects.count(),
        "num_workers": get_user_model().objects.count()
    }
    return render(request, "task_manager/index.html", context=context)


class TaskTypeListView(generic.ListView):
    model = TaskType
    template_name = "templates/task_type_list.html"
    context_object_name = "task_types_list"


class PositionListView(generic.ListView):
    model = Position
