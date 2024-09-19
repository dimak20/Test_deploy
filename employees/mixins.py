from django.views.generic import ListView
from django.db.models import Case, When, Q

from employees.forms import InvitationSearchForm
from employees.models import Invitation


class InvitationSearchMixin(ListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        form = InvitationSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            if query:
                queryset = queryset.annotate(
                    email_match=Case(
                        When(email__icontains=query, then=1),
                        default=0,
                    ),
                    position_match=Case(
                        When(position__name__icontains=query, then=1),
                        default=0,
                    )
                ).filter(
                    Q(email__icontains=query) | Q(position__name__icontains=query)
                ).order_by('-email_match', '-position_match')

        return queryset