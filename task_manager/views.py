from typing import Dict, Any

from django.shortcuts import render
from django.views import generic

from task_manager.models import Task, Worker, Project, Team, Position


def index(request):
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    num_projects = Project.objects.count()
    num_teams = Team.objects.count()
    num_positions = Position.objects.count()
    num_incomplete_projects = Project.objects.filter(is_complete=False).count()
    num_completed_projects = Project.objects.filter(is_complete=True).count()
    num_incomplete_tasks = Task.objects.filter(is_complete=False).count()
    num_completed_tasks = Task.objects.filter(is_complete=True).count()
    percent_tasks_completed = (num_completed_tasks / num_tasks) * 100
    percent_projects_completed = (num_completed_projects / num_projects) * 100
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    cards = [
        {
            "name": "Projects in work",
            "icon_name": "ui-checks-grid",
            "num_value": num_incomplete_projects
        },
        {
            "name": "Completed projects",
            "icon_name": "check-square",
            "num_value": num_completed_projects
        },
        {
            "name": "Tasks in work",
            "icon_name": "list-task",
            "num_value": num_incomplete_tasks
        },
        {
            "name": "Completed tasks",
            "icon_name": "list-check",
            "num_value": num_completed_tasks
        },
        {
            "name": "Workers",
            "icon_name": "people-fill",
            "num_value": num_workers
        },
        {
            "name": "Best teams",
            "icon_name": "person-arms-up",
            "num_value": num_teams
        },
        {
            "name": "Positions",
            "icon_name": "emoji-sunglasses-fill",
            "num_value": num_positions
        },
        {
            "name": "Page visits",
            "icon_name": "file-earmark",
            "num_value": num_visits
        },
    ]

    context = {
        "percent_tasks_completed": percent_tasks_completed,
        "percent_projects_completed": percent_projects_completed,
        "main_page_cards": cards,
    }

    return render(request, "index.html", context=context)


class ProjectListView(generic.ListView):
    model = Project
    context_object_name = "project_list"
    template_name = "task_manager/projects_list.html"

    def get_queryset(self):
        return Project.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_list = Project.objects.prefetch_related("tasks").all()
        num_completed_projects = project_list.filter(is_complete=True).count()
        num_projects = project_list.count()

        if num_projects > 0:
            percent_projects_completed = (
                                                     num_completed_projects / num_projects) * 100
        else:
            percent_projects_completed = 0

        context["project_list"] = project_list
        context["percent_projects_completed"] = percent_projects_completed

        return context


class TaskListView(generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "task_manager/task_list.html"

    def get_queryset(self):
        return Project.objects.all()

    def get_context_data(self, **kwargs):
        project_list = Project.objects.prefetch_related("tasks").all()
        num_completed_projects = project_list.filter(is_complete=True).count()
        num_projects = project_list.count()

        if num_projects > 0:
            percent_projects_completed = (
                            num_completed_projects / num_projects
                            ) * 100
        else:
            percent_projects_completed = 0

        context["project_list"] = project_list
        context["percent_projects_completed"] = percent_projects_completed

        return context
