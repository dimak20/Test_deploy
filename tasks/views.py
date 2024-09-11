from django.db.models import Case, When, Value, IntegerField, Q
from django.views import generic

from tasks.forms import TaskSearchForm
from tasks.models import Project


class ProjectCreateView(generic.CreateView):
    model = Project
    fields = ("name", "description")


class ProjectDetailView(generic.DetailView):
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


class ProjectUpdateView(generic.UpdateView):
    model = Project


class ProjectDeleteView(generic.DeleteView):
    model = Project
