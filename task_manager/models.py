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


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_completed = models.BooleanField()
    deadline = models.DateField()
    team = models.OneToOneField(Team, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} (team: {self.team.name})"


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers",
        null=True,
        default=None,
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="workers",
        default=None,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"

    def finished_tasks(self) -> QuerySet:
        return self.tasks.filter(is_completed=True)

    def overdue_tasks(self) -> QuerySet:
        return self.tasks.filter(Q(deadline__lt=datetime.date.today()), Q(is_completed=False))


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
    tags = TaggableManager()

    def __str__(self) -> str:
        return f"{self.name} (priority: {self.priority}, deadline: {self.deadline})"

    def tags_left(self) -> int:
        count = self.tags.count() - 1
        return count if count > 0 else 0
