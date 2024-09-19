from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Case, When, Value, IntegerField, Q
from django.urls.base import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import render

from tasks.forms import TaskSearchForm, ProjectCreateForm
from tasks.mixins import ProjectSearchMixin
from tasks.models import Project


class UserDashboardView(LoginRequiredMixin, View):
    pass


class ProjectListView(LoginRequiredMixin, ProjectSearchMixin, ListView):
    model = Project
    paginate_by = 5


class ProjectCreateView(CreateView):
    model = Project
    template_name = "tasks/project_form.html"
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
    template_name = "tasks/project_detail.html"

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
