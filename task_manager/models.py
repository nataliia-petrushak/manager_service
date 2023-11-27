import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet, Q
from taggit.managers import TaggableManager


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)
    duties = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

    def duties_to_a_list(self) -> list:
        return list(self.duties.split(";"))[:-1]


class Team(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    def sum_of_budget(self) -> int:
        return sum(project.budget for project in self.projects.all())


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers",
        blank=True,
        null=True
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="workers",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"

    def finished_tasks(self) -> QuerySet:
        return self.tasks.filter(is_completed=True)

    def in_progress_tasks(self) -> QuerySet:
        return self.tasks.filter(
            Q(deadline__gt=datetime.date.today()) & Q(is_completed=False))

    def overdue_tasks(self) -> QuerySet:
        return self.tasks.filter(
            Q(deadline__lt=datetime.date.today()), Q(is_completed=False)
        )


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_completed = models.BooleanField()
    deadline = models.DateField()
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="projects"
    )
    budget = models.DecimalField(decimal_places=2, max_digits=8, default=0)

    def __str__(self) -> str:
        return self.name

    def progress(self) -> int:
        all_tasks = self.tasks.count()
        completed_tasks = self.tasks.filter(
            is_completed=True
        ).count()
        progress = 0
        if completed_tasks:
            progress = round(self.tasks.filter(
                is_completed=True
            ).count() / all_tasks * 10) * 10
        return progress


class Task(models.Model):

    PRIORITY_CHOICES = [
        ("H", "High"),
        ("M", "Medium"),
        ("L", "Low")
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    deadline = models.DateField()
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default="L"
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks",
        blank=True
    )
    tags = TaggableManager(blank=True)

    def __str__(self) -> str:
        return f"{self.name} (priority: {self.priority})"

    def tags_left(self) -> int:
        count = self.tags.count() - 1
        return count if count > 0 else 0
