from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import TaskType, Task, Worker, Position

admin.site.register(TaskType)
admin.site.register(Position)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Additional info", {"fields": ("position",)}),)
    list_filter = ("position",)
    search_fields = ("username",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "deadline", "is_completed", "priority", "task_type")
    list_filter = ("is_completed", "priority", "task_type")
    search_fields = ("name",)
