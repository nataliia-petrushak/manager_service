from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import (
    TaskForm,
    TaskTypeForm,
    TaskTypeSearchForm,
    PositionForm,
    PositionSearchForm
)
from .models import Task, TaskType, Position, Worker


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
    template_name = "task_manager/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(initial={
            "name": name
        })
        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()

        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskTypeCreate(generic.CreateView):
    model = TaskType
    form_class = TaskTypeForm
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeUpdate(generic.UpdateView):
    model = TaskType
    form_class = TaskTypeForm
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDelete(generic.DeleteView):
    model = TaskType
    template_name = "task_manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class PositionListView(generic.ListView):
    model = Position
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(initial={
            "name": name
        })
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Position.objects.all()
        form = PositionSearchForm(self.request.GET)

        if form.is_valid():
            queryset = Position.objects.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class PositionCreate(generic.CreateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("task_manager:position-list")


class PositionUpdate(generic.UpdateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("task_manager:position-list")


class PositionDelete(generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


class WorkerListView(generic.ListView):
    model = Worker
    queryset = get_user_model().objects.select_related("position")


class WorkerDetailView(generic.DetailView):
    model = Worker
    queryset = get_user_model().objects.select_related("position")


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type"
    ).prefetch_related("assignees")


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type"
    ).prefetch_related("assignees")


class TaskCreate(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdate(generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-detail")


class TaskDelete(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")
