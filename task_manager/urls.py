from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from task_manager.views import (
    index,
    ProjectListView,
    ProjectDetailView,
    ProjectTaskDeleteView,
    project_task_create,
    project_task_update,
    ProjectCreateView,
    ProjectDeleteView,
    ProjectUpdateView,
    TaskListView,
    TaskDetailView,
    TaskDeleteView,
    TaskUpdateView,
    TaskCreateView,
)


app_name = "task_manager"


urlpatterns = [
                  path(
                      "", index, name="index"
                  ),
                  path(
                      "tasks/",
                      TaskListView.as_view(),
                      name="tasks-list",
                  ),
                  path(
                      "task/<int:pk>",
                      TaskDetailView.as_view(),
                      name="tasks-detail",
                  ),
                  path(
                      "task/create",
                      TaskCreateView.as_view(),
                      name="task-create",
                  ),
                  path(
                      "task/<int:pk>/delete",
                      TaskDeleteView.as_view(),
                      name="task-delete",
                  ),
                  path(
                      "task/<int:pk>/update",
                      TaskUpdateView.as_view(),
                      name="task-update",
                  ),
                  path(
                      "projects/",
                      ProjectListView.as_view(),
                      name="projects-list",
                  ),
                  path(
                      "project/<int:pk>/",
                      ProjectDetailView.as_view(),
                      name="project-detail"),
                  path(
                      "project/create/",
                      ProjectCreateView.as_view(),
                      name="project-create"),
                  path(
                      "project/<int:pk>/delete/",
                      ProjectDeleteView.as_view(),
                      name="project-delete"),
                  path(
                      "project/<int:project_id>/update/",
                      ProjectUpdateView.as_view(),
                      name="project-update"),
                  path("project/<int:pk>/create_task/",
                       project_task_create, name="project-task-create"
                       ),
                  path("project/<int:project_id>/task_update/<int:task_id>/",
                       project_task_update, name="project-task-update"),
                  path('project/<int:project_id>/delete_task/<int:pk>/',
                       ProjectTaskDeleteView.as_view(),
                       name='project-task-delete'
                       ),
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)



