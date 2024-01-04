from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
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
admin.site.register(Project)
admin.site.register(Team)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "start_time",
        "deadline",
        "is_complete",
        "priority",
        "task_type",
    ]
    search_fields = ["name", ]
    list_filter = [
        "is_complete",
        "priority",
    ]


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
