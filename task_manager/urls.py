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
)

urlpatterns = [
                  path(
                      "", index, name="index"
                  ),
                  path(
                      "projects/",
                      ProjectListView.as_view(),
                      name="projects-list",
                  ),
                  path(
                      "projects/<int:pk>/",
                      ProjectDetailView.as_view(),
                      name="project-detail"),
                  path(
                      "projects/create/",
                      ProjectCreateView.as_view(),
                      name="project-create"),
                  path(
                      "projects/<int:project_id>/delete/",
                      ProjectDeleteView.as_view(),
                      name="project-delete"),
                  path(
                      "projects/<int:project_id>/update/",
                      ProjectUpdateView.as_view(),
                      name="project-update"),
                  path("projects/<int:pk>/create_task/",
                       project_task_create, name="project-task-create"
                       ),
                  path("projects/<int:project_id>/task_update/<int:task_id>/",
                       project_task_update, name="project-task-update"),
                  path('projects/<int:project_id>/delete_task/<int:pk>/',
                       ProjectTaskDeleteView.as_view(),
                       name='project-task-delete'
                       ),
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)

app_name = "task_manager"
