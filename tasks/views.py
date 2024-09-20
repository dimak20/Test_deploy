from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Case, When, Value, IntegerField, Q
from django.urls.base import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import render

from tasks.forms import TaskSearchForm, ProjectCreateForm, TaskCreateForm
from tasks.mixins import ProjectSearchMixin
from tasks.models import Project, Task


class UserDashboardView(LoginRequiredMixin, View):
    pass


class ProjectListView(LoginRequiredMixin, ProjectSearchMixin, ListView):
    model = Project
    paginate_by = 5
    template_name = "tasks/projects/project_list.html"


class ProjectCreateView(CreateView):
    model = Project
    template_name = "tasks/projects/project_form.html"
    form_class = ProjectCreateForm
    success_url = reverse_lazy("tasks:project-list")

    def form_valid(self, form):
        project = form.save()
        project_url = reverse("tasks:project-detail", kwargs={"slug": project.slug})
        message = mark_safe(f"<a style='text-decoration: underline;' href={project_url}>Project</a> created")
        messages.success(self.request, message)
        return super().form_valid(form)


class ProjectDetailView(DetailView):
    model = Project
    template_name = "tasks/projects/project_detail.html"

    def get_queryset(self):
        queryset = Project.objects.prefetch_related("tasks")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = self.get_object()
        tasks = project.tasks.all()

        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]

            tasks = tasks.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

            tasks = tasks.annotate(
                search_priority=Case(
                    When(name__icontains=query, then=Value(1)),
                    When(description__icontains=query, then=Value(2)),
                    output_field=IntegerField(),
                )
            ).order_by("search_priority")

        context["project"] = project
        context["tasks"] = tasks
        context["search_form"] = TaskSearchForm()
        return context


class ProjectUpdateView(UpdateView):
    model = Project


class ProjectDeleteView(DeleteView):
    model = Project


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "tasks/task_form.html"

    def form_valid(self, form):
        task = form.save(commit=False)
        project_slug = self.kwargs.get("project_slug")
        task.project = Project.objects.get(slug=project_slug)
        task.save()
        return super().form_valid(form)

    def get_success_url(self):
        project_slug = self.kwargs.get("project_slug")
        return reverse_lazy("tasks:project-detail", kwargs={"slug": project_slug})
