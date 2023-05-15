from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import TaskType, Task, Worker, Position, Project, Team


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "deadline", "is_completed", "team")
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", "team")
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("position", "team")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Additional info", {"fields": ("position", "team")}),)
    list_filter = ("team",)
    search_fields = ("username",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "deadline", "is_completed", "priority", "task_type", "tag_list")
    list_filter = ("is_completed", "priority", "task_type")
    search_fields = ("name",)

    def tag_list(self, obj):
        return ", ".join(o for o in obj.tags.names())


admin.site.register(Team)
admin.site.register(TaskType)
admin.site.register(Position)
admin.site.unregister(Group)
