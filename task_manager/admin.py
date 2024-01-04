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


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "display_projects",
        "start_time",
        "deadline",
        "is_complete",
        "priority",
    )
    search_fields = ("name",)
    list_filter = ("is_complete", "priority", "task_type",)
    date_hierarchy = "start_time"

    def display_projects(self, obj):
        return ', '.join([project.name for project in obj.projects.all()])

    display_projects.short_description = 'Projects'


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", "phone_number",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position", "phone_number")}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                        "phone_number"
                    )
                },
            ),
        )
    )
    list_filter = [
        "position",
    ]


class TeamInline(admin.TabularInline):
    model = Team.projects.through
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_task_list",
    )

    def get_task_list(self, obj):
        return ', '.join([task.name for task in obj.tasks.all()])

    get_task_list.short_description = "Tasks"

    inlines = [TeamInline]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "display_projects",
    )

    def display_projects(self, obj):
        return ', '.join([project.name for project in obj.projects.all()])

    display_projects.short_description = "Projects"


admin.site.unregister(Group)
