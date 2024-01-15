from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import ProjectTaskForm
from .utils import calculate_percentage
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
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    percent_tasks_completed = calculate_percentage(
        num_completed_tasks, num_tasks
    )
    percent_projects_completed = calculate_percentage(
        num_completed_projects, num_projects
    )

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
    template_name = "task_manager/projects/projects_list.html"

    def get_queryset(self) -> QuerySet[Project]:
        return Project.objects.all()

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        project_list = Project.objects.prefetch_related("tasks").all()
        num_completed_projects = project_list.filter(is_complete=True).count()
        num_projects = project_list.count()

        percent_projects_completed = calculate_percentage(
            num_completed_projects, num_projects
        )

        context["project_list"] = project_list
        context["percent_projects_completed"] = percent_projects_completed
        context["projects_info"] = self.get_projects_info(project_list)

        return context

    @staticmethod
    def get_projects_info(project_list) -> list:
        tasks_info = []
        for project in project_list:
            project_info = {
                "project_name": project.name,
                "tasks_info": [(task.name, task.is_complete) for task in
                               project.tasks.all()],
                "id": project.id,
                "task_names": [],
                "deadlines": [],
                "priorities": []
            }
            for task in project.tasks.all():
                project_info["task_names"].append(task.name)
                project_info["deadlines"].append(task.deadline)
                project_info["priorities"].append(task.priority)
            tasks_info.append(project_info)
        return tasks_info


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'task_manager/projects/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks_list = self.object.tasks.all()
        context["project_workers"] = self.object.teams.first().workers.all()
        context["project_tasks"] = self.get_tasks_info(tasks_list)
        return context

    @staticmethod
    def get_tasks_info(tasks_list) -> list:
        tasks_info = []
        for task in tasks_list:
            task_info = {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "start_time": task.start_time,
                "is_complete": task.is_complete,
                "deadline": task.deadline,
                "priority": task.priority,
                "task_types": task.task_type.all()
            }
            tasks_info.append(task_info)
        return tasks_info


def project_task_create(request, pk):
    project = Project.objects.get(pk=pk)

    if request.method == 'POST':
        form = ProjectTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect(
                "task_manager:project-detail",
                pk=project.id
            )
    else:
        form = ProjectTaskForm()

    return render(request,
                  'task_manager/projects/project_task_create_update.html',
                  {'form': form, 'project': project, "name": "create"}, )


def project_task_update(request, project_id, task_id):
    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, project=project)

    if request.method == 'POST':
        form = ProjectTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_manager:project-detail", pk=project.id)
    else:
        form = ProjectTaskForm(instance=task)

    return render(request,
                  'task_manager/projects/project_task_create_update.html',
                  {'form': form, 'project': project, "name": "update"})


class ProjectTaskDeleteView(generic.DeleteView):
    model = Task
    template_name = 'task_manager/projects/project_task_delete.html'
    context_object_name = 'task'

    def get_success_url(self):
        project_id = self.kwargs.get('project_id')
        return reverse_lazy('task_manager:project-detail',
                            kwargs={'pk': project_id})

    def get_object(self, queryset=None):
        project_id = self.kwargs.get('project_id')
        task_id = self.kwargs.get('pk')
        project = get_object_or_404(Project, id=project_id)
        task = get_object_or_404(Task, id=task_id, project=project)
        return task
