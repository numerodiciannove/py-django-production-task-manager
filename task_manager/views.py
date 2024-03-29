from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import (
    ProjectTaskForm,
    ProjectForm,
    TaskForm,
    WorkerForm,
    TeamForm,
    PositionForm,
    WorkerSearchForm,
    TeamSearchForm,
    PositionSearchForm,
)
from .utils import calculate_percentage
from task_manager.models import Task, Worker, Project, Team, Position


def index(request):
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    num_projects = Project.objects.count()
    num_teams = Team.objects.count()
    num_positions = Position.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    aggregate_data = Project.objects.aggregate(
        num_incomplete_projects=Count("id", filter=Q(is_complete=False)),
        num_completed_projects=Count("id", filter=Q(is_complete=True)),
        num_incomplete_tasks=Count("id", filter=Q(is_complete=False)),
        num_completed_tasks=Count("id", filter=Q(is_complete=True)),
    )

    cards = [
        {
            "name": "Projects in work",
            "icon_name": "ui-checks-grid",
            "num_value": aggregate_data["num_incomplete_projects"],
        },
        {
            "name": "Completed projects",
            "icon_name": "check-square",
            "num_value": aggregate_data["num_completed_projects"],
        },
        {
            "name": "Tasks in work",
            "icon_name": "list-task",
            "num_value": aggregate_data["num_incomplete_tasks"],
        },
        {
            "name": "Completed tasks",
            "icon_name": "list-check",
            "num_value": aggregate_data["num_completed_tasks"],
        },
        {"name": "Workers", "icon_name": "people-fill",
         "num_value": num_workers},
        {"name": "Best teams", "icon_name": "person-arms-up",
         "num_value": num_teams},
        {
            "name": "Positions",
            "icon_name": "emoji-sunglasses-fill",
            "num_value": num_positions,
        },
        {"name": "Page visits", "icon_name": "file-earmark",
         "num_value": num_visits},
    ]

    percent_tasks_completed = calculate_percentage(
        aggregate_data["num_completed_tasks"], num_tasks
    )
    percent_projects_completed = calculate_percentage(
        aggregate_data["num_completed_projects"], num_projects
    )

    context = {
        "percent_tasks_completed": percent_tasks_completed,
        "percent_projects_completed": percent_projects_completed,
        "main_page_cards": cards,
    }

    return render(request, "index.html", context=context)


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    context_object_name = "project_list"
    template_name = "task_manager/projects/projects_list.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        project_list = Project.objects.prefetch_related("tasks").all()
        num_completed_projects = project_list.filter(is_complete=True).count()
        num_projects = project_list.count()

        percent_projects_completed = calculate_percentage(
            num_completed_projects, num_projects
        )

        sorted_project_list = sorted(
            project_list,
            key=lambda project: (
                project.is_complete,
                project.name,
            ),
        )

        context["project_list"] = sorted_project_list
        context["percent_projects_completed"] = percent_projects_completed
        context["projects_info"] = self.get_project_info(sorted_project_list)

        return context

    @staticmethod
    def get_project_info(project_list) -> list:
        project_info = []
        for project in project_list:
            teams_info = project.teams.all()
            tasks_sorted = sorted(
                project.tasks.all(),
                key=lambda task: (
                    task.is_complete,
                    task.name,
                ),
            )
            project_info.append(
                {
                    "project_name": project.name,
                    "tasks_info": [
                        {
                            "task_id": task.id,
                            "task_name": task.name,
                            "is_complete": task.is_complete,
                        }
                        for task in tasks_sorted
                    ],
                    "id": project.id,
                    "task_names": [task.name for task in tasks_sorted],
                    "tasks_start_time": [task.start_time for task in
                                         tasks_sorted],
                    "deadlines": [task.deadline for task in tasks_sorted],
                    "priorities": [task.priority for task in tasks_sorted],
                    "is_complete": project.is_complete,
                    "teams_info": list(teams_info),
                }
            )
        return project_info


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    template_name = "task_manager/projects/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks_list = self.object.tasks.all()
        context["project_tasks"] = self.get_tasks_info(tasks_list)

        team = self.object.teams.first()
        context["project_workers"] = team.workers.all() if team else []

        return context

    @staticmethod
    def get_tasks_info(tasks_list) -> list:
        tasks_info = []
        for task in tasks_list:
            task_info = {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "start_time": task.start_time if task.start_time else "-",
                "is_complete": task.is_complete,
                "deadline": task.deadline if task.deadline else "-",
                "priority": task.priority,
                "task_types": task.task_type.all(),
            }
            tasks_info.append(task_info)
        return tasks_info


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "task_manager/projects/project_create_update.html"
    success_url = reverse_lazy("task_manager:projects-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "update" if self.object else "create"
        return context


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "task_manager/projects/project_create_update.html"
    context_object_name = "project"

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:projects-list",
        )

    def get_object(self, queryset=None):
        project_id = self.kwargs.get("project_id")
        project = get_object_or_404(Project, id=project_id)
        return project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "update" if self.object else "create"
        return context


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    template_name = "task_manager/projects/project_delete.html"
    success_url = reverse_lazy("task_manager:projects-list")


class ProjectTaskCreateView(generic.CreateView):
    model = Project
    form_class = ProjectTaskForm
    template_name = "task_manager/tasks/task_create_update.html"
    context_object_name = "project"

    def form_valid(self, form):
        project = self.get_object()
        task = form.save(commit=False)
        task.project = project
        task.save()
        return redirect("task_manager:project-detail", pk=project.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "create"
        return context

    def get_success_url(self):
        return reverse("task_manager:project-detail",
                       kwargs={"pk": self.object.id})


class ProjectTaskUpdateView(generic.UpdateView):
    model = Task
    form_class = ProjectTaskForm
    template_name = "task_manager/tasks/task_create_update.html"
    context_object_name = "project"

    def get_object(self, queryset=None):
        project_id = self.kwargs.get("project_id")
        task_id = self.kwargs.get("task_id")
        return get_object_or_404(Task, pk=task_id, project__pk=project_id)

    def form_valid(self, form):
        project = self.get_object().project
        form.save()
        return redirect("task_manager:project-detail", pk=project.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "update"
        return context

    def get_success_url(self):
        project = self.get_object().project
        return reverse("task_manager:project-detail",
                       kwargs={"pk": project.id})


class ProjectTaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task_manager/tasks/task_delete.html"
    context_object_name = "task"

    def get_success_url(self):
        project_id = self.kwargs.get("project_id")
        return reverse_lazy("task_manager:project-detail",
                            kwargs={"pk": project_id})

    def get_object(self, queryset=None):
        project_id = self.kwargs.get("project_id")
        task_id = self.kwargs.get("pk")
        project = get_object_or_404(Project, id=project_id)
        task = get_object_or_404(Task, id=task_id, project=project)
        return task


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "task_manager/tasks/tasks_list.html"

    def get_queryset(self):
        return Task.objects.all().order_by("start_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks_list = Task.objects.all()
        num_completed_tasks = tasks_list.filter(is_complete=True).count()
        num_tasks = tasks_list.count()
        percent_tasks_completed = calculate_percentage(num_completed_tasks,
                                                       num_tasks)

        context["percent_tasks_completed"] = percent_tasks_completed
        context["num_completed_tasks"] = num_completed_tasks
        context["task_info"] = self.get_task_info(tasks_list)

        return context

    @staticmethod
    def get_task_info(task_list):
        task_info = []

        for task in task_list:
            teams_info = task.project.teams.all()
            tasks_sorted = sorted(task.project.tasks.all(),
                                  key=lambda t: (t.project,))
            task_info.append(
                {
                    "project_name": task.project.name,
                    "project_id": task.project.id,
                    "name": task.name,
                    "task_types": [
                        task_type.name for task_type in task.task_type.all()
                    ],
                    "is_complete": task.is_complete,
                    "id": task.id,
                    "task_names": [t.name for t in tasks_sorted],
                    "task_start_time": task.start_time,
                    "deadlines": task.deadline,
                    "priorities": task.priority,
                    "teams_info": list(teams_info),
                }
            )
        return task_info


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "task_manager/tasks/task_detail.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("project__teams", "project__teams__workers")
            .all()
        )


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task_manager/tasks/task_delete.html"
    success_url = reverse_lazy("task_manager:tasks-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager/tasks/task_create_update.html"
    success_url = reverse_lazy("task_manager:tasks-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "update" if self.object else "create"
        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager/tasks/task_create_update.html"
    success_url = reverse_lazy("task_manager:tasks-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "update" if self.object else "create"
        return context


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "worker_list"
    template_name = "task_manager/workers/workers_list.html"
    paginate_by = 15

    def get_queryset(self):
        queryset = Worker.objects.prefetch_related("teams__projects", "teams")

        if self.request.GET.get("search_first_last_name"):
            search_query = self.request.GET.get("search_first_last_name")
            queryset = queryset.filter(
                Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workers_list = context["worker_list"]
        paginator = Paginator(workers_list, self.paginate_by)

        page = self.request.GET.get("page")
        paged_workers = paginator.get_page(page)

        positions_names = Worker.objects.values_list(
            "position__name", flat=True
        ).distinct()

        workers_info = []
        context["search_form"] = WorkerSearchForm()

        for worker in paged_workers:
            worker_projects_list = worker.teams.all().values_list(
                "projects__name", "projects__id"
            )
            worker_projects = [
                {"name": name, "id": id} for name, id in worker_projects_list
            ]
            worker_teams = worker.teams.all()
            workers_info.append(
                {
                    "projects": worker_projects,
                    "phone_number": worker.phone_number,
                    "email": worker.email,
                    "position": (
                        worker.position.name if worker.position else None),
                    "country": worker.country,
                    "first_name": worker.first_name,
                    "last_name": worker.last_name,
                    "id": worker.id,
                    "teams": worker_teams,
                }
            )

        context["workers_list"] = paged_workers
        context["positions_names"] = positions_names
        context["workers_info"] = workers_info

        return context


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    context_object_name = "worker"
    template_name = "task_manager/workers/worker_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.get_object()
        projects = Project.objects.filter(teams__workers=worker).distinct()
        tasks_in_projects = Task.objects.filter(project__in=projects)

        context["projects"] = projects
        context["tasks_in_projects"] = tasks_in_projects
        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerForm
    template_name = "task_manager/workers/worker_create_update.html"
    success_url = reverse_lazy("task_manager:workers-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "update" if self.object else "create"
        return context


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = "task_manager/workers/worker_delete.html"
    success_url = reverse_lazy("task_manager:workers-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerForm
    template_name = "task_manager/workers/worker_create_update.html"
    success_url = reverse_lazy("task_manager:workers-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "update" if self.object else "create"
        return context


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    context_object_name = "team_list"
    template_name = "task_manager/teams/teams_list.html"

    def get_queryset(self):
        queryset = Team.objects.annotate(
            num_projects=Count("projects")).order_by(
            "-num_projects", "name"
        )

        search_query = self.request.GET.get("search_by_team_name")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teams_list = self.get_queryset()
        teams_info = []

        for team in teams_list:
            projects_info = []
            projects = team.projects.all()

            for project in projects:
                tasks_info = []
                tasks = project.tasks.all()

                for task in tasks:
                    tasks_info.append(
                        {
                            "name": task.name,
                            "id": task.id,
                        }
                    )

                projects_info.append(
                    {
                        "project_name": project.name,
                        "project_id": project.id,
                        "tasks": tasks_info,
                    }
                )

            teams_info.append(
                {
                    "team_name": team.name,
                    "team_id": team.id,
                    "projects": projects_info,
                }
            )

        context["teams_info"] = teams_info
        context["search_form"] = TeamSearchForm()
        return context


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    context_object_name = "team"
    template_name = "task_manager/teams/team_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        team_members = team.workers.all()
        team_projects = team.projects.all()
        context["team_members"] = team_members
        context["team_projects"] = team_projects

        return context


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm
    template_name = "task_manager/teams/team_create_update.html"
    success_url = reverse_lazy("task_manager:teams-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "update" if self.object else "create"
        return context


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm
    template_name = "task_manager/teams/team_create_update.html"
    success_url = reverse_lazy("task_manager:teams-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "update" if self.object else "create"
        return context


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    template_name = "task_manager/teams/team_delete.html"
    success_url = reverse_lazy("task_manager:teams-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "position_list"
    template_name = "task_manager/positions/positions_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = Position.objects.all()

        search_query = self.request.GET.get("search_by_position")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = PositionSearchForm()
        return context


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    template_name = "task_manager/positions/position_delete.html"
    success_url = reverse_lazy("task_manager:positions-list")


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionForm
    template_name = "task_manager/positions/position_create_update.html"
    success_url = reverse_lazy("task_manager:positions-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionForm
    template_name = "task_manager/positions/position_create_update.html"
    success_url = reverse_lazy("task_manager:positions-list")
