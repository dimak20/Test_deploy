from django.urls import path

from tasks.views import ProjectListView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView

app_name = "tasks"

urlpatterns = [
    path("tasks/", ProjectListView.as_view(), name="project-list"),
    path("projects/create/", ProjectCreateView.as_view(), name="project-create"),
    path("projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"),
    path("projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"),
]