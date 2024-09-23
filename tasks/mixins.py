from django.db.models import Case, When, Q
from django.views.generic import ListView

from tasks.forms import ProjectSearchForm


class ProjectSearchMixin(ListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        form = ProjectSearchForm(self.request.GET)

        if form.is_valid():
            query = form.cleaned_data["query"]
            if query:
                queryset = (
                    queryset.annotate(
                        name_match=Case(
                            When(name__icontains=query, then=1),
                            default=0,
                        ),
                        task_match=Case(
                            When(tasks__name__icontains=query, then=1),
                            default=0,
                        ),
                    )
                    .filter(Q(name__icontains=query) | Q(tasks__name__icontains=query))
                    .order_by("-name_match", "-task_match")
                )

        return queryset
