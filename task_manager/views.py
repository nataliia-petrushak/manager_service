from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Q, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from taggit.models import Tag

from .forms import (
    TaskForm,
    TaskTypeForm,
    TaskTypeSearchForm,
    PositionForm,
    PositionSearchForm,
    WorkerCreateForm
)
from .models import Task, TaskType, Position, Worker, Project, Team


def index(request):
    """View function for the home page of the site."""

    context = {
        "num_teams": Team.objects.count(),
        "num_projects": Project.objects.count(),
        "num_workers": get_user_model().objects.count()
    }
    return render(request, "task_manager/index.html", context=context)


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
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


class TaskTypeCreate(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TaskTypeForm
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeUpdate(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = TaskTypeForm
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDelete(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task_manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
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


class PositionCreate(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("task_manager:position-list")


class PositionUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("task_manager:position-list")


class PositionDelete(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = get_user_model().objects.select_related("position")


class WorkerCreate(generic.CreateView):
    model = Worker
    form_class = WorkerCreateForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("task_manager:index")


class WorkerUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerCreateForm
    template_name = "task_manager/worker_update.html"
    success_url = reverse_lazy("task_manager:index")


class WorkerDelete(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:index")


@login_required
def toggle_assign_to_task(request, pk):
    assignee = get_user_model().objects.get(id=request.user.id)
    if (
        get_user_model().objects.get(id=pk) in assignee.tasks.all()
    ):  # probably could check if car exists
        assignee.tasks.remove(pk)
    else:
        assignee.tasks.add(pk)
    return HttpResponseRedirect(reverse_lazy("task_manager:task-detail", args=[pk]))


@login_required
def tasks_of_project_by_tags(request, pk: int, slug: str = None):
    project = get_object_or_404(Project, pk=pk)
    task_list = project.tasks.annotate(assignees_count=Count("assignees"))
    if slug:
        tag = get_object_or_404(Tag, slug=slug)
        task_list = task_list.filter(tags=tag)
    context = {
        "project": project,
        "task_list": task_list,
        "tags": Task.tags.filter(task__project=project),
        "to_do": task_list.filter(assignees_count=0),
        "in_process": task_list.filter(
            Q(is_completed=False) & Q(assignees_count__gt=0)
        ),
        "completed": task_list.filter(is_completed=True),
        "id": pk
    }

    return render(request, "task_manager/task_list.html", context)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type"
    ).prefetch_related("assignees")


class TaskCreate(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("task_manager:project-tasks", kwargs={
            "pk": self.request.POST.get("project")
        })


class TaskUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("task_manager:project-tasks", kwargs={
            "pk": self.request.POST.get("project")
        })


class TaskDelete(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:index")


def dashboard(request):

    user_info = sorted([
        [user, user.finished_tasks().count()]
        for user in get_user_model().objects.all()
    ], key=lambda x: x[1], reverse=True)

    teams = Team.objects.annotate(projects_count=Count("projects"))

    context = {
        "projects": Project.objects.select_related("team"),
        "users": user_info[:10],
        "teams": teams
    }

    return render(request, "task_manager/dashboard.html", context)
