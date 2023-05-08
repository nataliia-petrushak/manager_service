import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet, Q


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers",
        default=1
    )

    def __str__(self) -> str:
        return f"{self.username} (position: {self.position.name})"

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

    def __str__(self) -> str:
        return f"{self.name} (priority: {self.priority}, deadline: {self.deadline})"

    def days_to_deadline(self) -> int:
        return (self.deadline - datetime.date.today()).days
