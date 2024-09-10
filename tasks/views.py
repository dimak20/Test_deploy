from django.shortcuts import render
from django.views import generic

from tasks.models import Project


class ProjectListView(generic.ListView):
    model = Project


class ProjectCreateView(generic.CreateView):
    model = Project
    fields = ("name", "description")


class ProjectUpdateView(generic.UpdateView):
    model = Project


class ProjectDeleteView(generic.DeleteView):
    model = Project