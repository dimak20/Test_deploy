from django.shortcuts import render, get_object_or_404
from django.views import generic

from tasks.models import Project


class ProjectCreateView(generic.CreateView):
    model = Project
    fields = ("name", "description")


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = "tasks/project_detail.html"


class ProjectUpdateView(generic.UpdateView):
    model = Project


class ProjectDeleteView(generic.DeleteView):
    model = Project
