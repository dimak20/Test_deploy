from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Case, When, Value, IntegerField, Q, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import (
    View,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from employees.models import Team
from tasks.forms import TaskSearchForm, ProjectForm, TaskForm
from tasks.mixins import ProjectSearchMixin
from tasks.models import Project, Task


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "tasks/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        projects_by_tasks = Project.objects.filter(
            tasks__assignees=self.request.user
        ).distinct()
        projects_by_teams = Project.objects.filter(
            teams__members=self.request.user
        ).distinct()
        context["user_projects"] = projects_by_tasks | projects_by_teams.exclude(
            id__in=projects_by_tasks.values("id")
        )

        teams = Team.objects.filter(members=self.request.user).distinct()
        context["user_teams"] = teams

        context["user_tasks"] = (
            Task.objects.filter(assignees=self.request.user)
            .distinct()
            .select_related("project")
            .order_by("deadline")
        )

        return context


# Project Views
class ProjectListView(LoginRequiredMixin, ProjectSearchMixin, ListView):
    model = Project
    queryset = Project.objects.prefetch_related("tasks", "teams")
    paginate_by = 5
    template_name = "tasks/projects/project_list.html"

    def get_queryset(self):
        return Project.objects.prefetch_related("tasks", "teams").annotate(
            active_tasks_num=Count("tasks", filter=Q(tasks__is_completed=False)),
            completed_tasks_num=Count("tasks", filter=Q(tasks__is_completed=True)),
        )


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = "tasks/projects/project_form.html"
    form_class = ProjectForm
    success_url = reverse_lazy("tasks:project-list")

    def form_valid(self, form):
        project = form.save()
        project_url = reverse("tasks:project-detail", kwargs={"slug": project.slug})
        message = mark_safe(
            f"<a style='text-decoration: underline;' href='{project_url}'>Project</a> created"
        )
        messages.success(self.request, message)
        return super().form_valid(form)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "tasks/projects/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = self.get_object()
        tasks = (
            project.tasks.select_related("task_type")
            .prefetch_related("assignees", "tags")
            .all()
        )

        form = TaskSearchForm(self.request.GET)
        if self.request.GET.get("query"):
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


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = "tasks/projects/project_form.html"
    form_class = ProjectForm
    success_url = reverse_lazy("tasks:project-list")


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "tasks/projects/project_confirm_delete.html"


# Task Views
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"

    def form_valid(self, form):
        task = form.save(commit=False)
        project_slug = self.kwargs.get("project_slug")
        task.project = Project.objects.get(slug=project_slug)
        task.save()
        task_url = reverse("tasks:task-detail", kwargs={"slug": task.slug})
        message = mark_safe(
            f"<a style='text-decoration: underline;' href={task_url}>Task</a> created"
        )
        messages.success(self.request, message)
        return super().form_valid(form)

    def get_success_url(self):
        project_slug = self.kwargs.get("project_slug")
        return reverse_lazy("tasks:project-detail", kwargs={"slug": project_slug})


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    queryset = Task.objects


@login_required
def toggle_task_completion(request, slug):
    task = get_object_or_404(Task, slug=slug)

    if request.method == "POST":

        task.is_completed = not task.is_completed

        if task.is_completed:
            task.completed_by = request.user
        else:
            task.completed_by = None

        task.save()

    return redirect(reverse("tasks:task-detail", kwargs={"slug": slug}))


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"

    def get_success_url(self):
        return reverse("tasks:task-detail", kwargs={"slug": self.object.slug})


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"

    def get_success_url(self):
        project_slug = self.object.project.slug
        return reverse_lazy("tasks:project-detail", kwargs={"slug": project_slug})
