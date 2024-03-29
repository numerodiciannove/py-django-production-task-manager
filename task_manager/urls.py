from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from task_manager.views import (
    index,
    ProjectListView,
    ProjectDetailView,
    ProjectTaskDeleteView,
    ProjectCreateView,
    ProjectDeleteView,
    ProjectUpdateView,
    TaskListView,
    TaskDetailView,
    TaskDeleteView,
    TaskUpdateView,
    TaskCreateView,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    WorkerDeleteView,
    WorkerUpdateView,
    TeamListView,
    TeamDetailView,
    TeamUpdateView,
    TeamCreateView,
    TeamDeleteView,
    PositionListView,
    PositionDeleteView,
    PositionCreateView,
    PositionUpdateView,
    ProjectTaskCreateView,
    ProjectTaskUpdateView,
)

app_name = "task_manager"

urlpatterns = [
                  path("", index, name="index"),
                  path(
                      "tasks/",
                      TaskListView.as_view(),
                      name="tasks-list",
                  ),
                  path(
                      "task/<int:pk>/",
                      TaskDetailView.as_view(),
                      name="task-detail",
                  ),
                  path(
                      "task/create/",
                      TaskCreateView.as_view(),
                      name="task-create",
                  ),
                  path(
                      "task/<int:pk>/delete/",
                      TaskDeleteView.as_view(),
                      name="task-delete",
                  ),
                  path(
                      "task/<int:pk>/update/",
                      TaskUpdateView.as_view(),
                      name="task-update",
                  ),
                  path(
                      "projects/",
                      ProjectListView.as_view(),
                      name="projects-list",
                  ),
                  path("project/<int:pk>/", ProjectDetailView.as_view(),
                       name="project-detail"),
                  path("project/create/", ProjectCreateView.as_view(),
                       name="project-create"),
                  path(
                      "project/<int:pk>/delete/", ProjectDeleteView.as_view(),
                      name="project-delete"
                  ),
                  path(
                      "project/<int:project_id>/update/",
                      ProjectUpdateView.as_view(),
                      name="project-update",
                  ),
                  path(
                      "project/<int:pk>/create_task/",
                      ProjectTaskCreateView.as_view(),
                      name="project-task-create",
                  ),
                  path(
                      "project/<int:project_id>/task_update/<int:task_id>/",
                      ProjectTaskUpdateView.as_view(),
                      name="project-task-update",
                  ),
                  path(
                      "project/<int:project_id>/delete_task/<int:pk>/",
                      ProjectTaskDeleteView.as_view(),
                      name="project-task-delete",
                  ),
                  path(
                      "workers/",
                      WorkerListView.as_view(),
                      name="workers-list",
                  ),
                  path("worker/<int:pk>/", WorkerDetailView.as_view(),
                       name="worker-detail"),
                  path("worker/create/", WorkerCreateView.as_view(),
                       name="worker-create"),
                  path("worker/<int:pk>/update/", WorkerUpdateView.as_view(),
                       name="worker-update"),
                  path("worker/<int:pk>/delete/", WorkerDeleteView.as_view(),
                       name="worker-delete"),
                  path(
                      "teams/",
                      TeamListView.as_view(),
                      name="teams-list",
                  ),
                  path("team/<int:pk>/", TeamDetailView.as_view(),
                       name="team-detail"),
                  path("team/<int:pk>/update/", TeamUpdateView.as_view(),
                       name="team-update"),
                  path("team/create/", TeamCreateView.as_view(),
                       name="team-create"),
                  path("team/<int:pk>/delete/", TeamDeleteView.as_view(),
                       name="team-delete"),
                  path(
                      "positions/",
                      PositionListView.as_view(),
                      name="positions-list",
                  ),
                  path(
                      "position/<int:pk>/delete/",
                      PositionDeleteView.as_view(),
                      name="position-delete",
                  ),
                  path("position/create/", PositionCreateView.as_view(),
                       name="position-create"),
                  path(
                      "position/<int:pk>:/update/",
                      PositionUpdateView.as_view(),
                      name="position-update",
                  ),
                  path("accounts/", include("django.contrib.auth.urls")),
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)
