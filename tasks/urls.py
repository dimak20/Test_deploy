from django.urls import path

from tasks.views import ProjectCreateView, ProjectUpdateView, ProjectDeleteView, ProjectDetailView

app_name = "tasks"

urlpatterns = [
    path("projects/create/", ProjectCreateView.as_view(), name="project-create"),
    path("projects/<slug:slug>/", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/<slug:slug>/update/", ProjectUpdateView.as_view(), name="project-update"),
    path("projects/<slug:slug>/delete/", ProjectDeleteView.as_view(), name="project-delete"),
]