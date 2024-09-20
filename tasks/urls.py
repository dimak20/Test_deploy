from django.urls import path

from tasks.views import ProjectCreateView, ProjectUpdateView, ProjectDeleteView, ProjectDetailView, ProjectListView, \
    TaskCreateView

app_name = "tasks"

urlpatterns = [
    # Projects
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("projects/create/", ProjectCreateView.as_view(), name="project-create"),
    path("projects/<slug:slug>/", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/<slug:slug>/update/", ProjectUpdateView.as_view(), name="project-update"),
    path("projects/<slug:slug>/delete/", ProjectDeleteView.as_view(), name="project-delete"),

    # Tasks
    path("tasks/create/<slug:project_slug>/", TaskCreateView.as_view(), name="task-create"),
]