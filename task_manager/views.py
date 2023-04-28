from django.contrib.auth import get_user_model
from django.shortcuts import render

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
