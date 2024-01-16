from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from task_manager.models import (
    Position,
    TaskType,
    Task,
    Worker,
    Project,
    Team
)

admin.site.register(Position)
admin.site.register(TaskType)


class TeamInline(admin.TabularInline):
    model = Team.projects.through
    extra = 1


class TaskInline(admin.StackedInline):
    model = Task
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_time",
        "deadline",
        "is_complete",
        "priority",
    )
    search_fields = ("name",)
    list_filter = ("is_complete", "priority", "task_type")
    filter_horizontal = ("task_type",)
    date_hierarchy = "start_time"


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "position",
        "phone_number",
        "country",
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            ("Additional info", {
                "fields": ("position", "phone_number", "country")
            }
             ),
        )
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "position",
                        "phone_number",
                        "country",
                    )
                },
            ),
        )
    )
    list_filter = [
        "position",
        "country",
    ]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_task_list",
        "is_complete",
        "budget",
    )
    search_fields = ("name", )
    list_filter = ("is_complete", )

    def get_task_list(self, obj):
        return ', '.join([task.name for task in obj.tasks.all()])

    get_task_list.short_description = "Tasks"
    inlines = [TeamInline, TaskInline]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "display_projects",
        "display_workers",
    )
    filter_horizontal = ("workers",)
    search_fields = ("name", )
    list_filter = ("name", "projects")

    def display_projects(self, obj):
        return ', '.join([project.name for project in obj.projects.all()])

    display_projects.short_description = "Projects"

    def display_workers(self, obj):
        return ', '.join(
            [f"{worker.position}" for worker in obj.workers.all()])

    display_workers.short_description = "Workers positions"


admin.site.unregister(Group)
