from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from task_manager.views import index, ProjectListView, ProjectDetailView

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
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name = "task_manager"
