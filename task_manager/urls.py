from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from task_manager.views import index, ProjectListView

urlpatterns = [
    path(
        "", index, name="index"
    ),
    path(
        "projects/",
        ProjectListView.as_view(),
        name="projects-list",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name = "task_manager"
