from django.views.generic import ListView
from django.db.models import Case, When, Q

from employees.forms import InvitationSearchForm, EmployeeSearchForm, TeamSearchForm


class InvitationSearchMixin(ListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        form = InvitationSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            if query:
                queryset = (
                    queryset.annotate(
                        email_match=Case(
                            When(email__icontains=query, then=1),
                            default=0,
                        ),
                        position_match=Case(
                            When(position__name__icontains=query, then=1),
                            default=0,
                        ),
                    )
                    .filter(
                        Q(email__icontains=query) | Q(position__name__icontains=query)
                    )
                    .order_by("-email_match", "-position_match")
                )

        return queryset


class EmployeeSearchMixin(ListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        form = EmployeeSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            if query:
                queryset = (
                    queryset.annotate(
                        email_match=Case(
                            When(email__icontains=query, then=1),
                            default=0,
                        ),
                        first_name_match=Case(
                            When(first_name__icontains=query, then=1),
                            default=0,
                        ),
                        last_name_match=Case(
                            When(last_name__icontains=query, then=1),
                            default=0,
                        ),
                        position_match=Case(
                            When(position__name__icontains=query, then=1),
                            default=0,
                        ),
                    )
                    .filter(
                        Q(email__icontains=query)
                        | Q(position__name__icontains=query)
                        | Q(first_name__icontains=query)
                        | Q(last_name__icontains=query)
                    )
                    .order_by(
                        "-last_name_match",
                        "-first_name_match",
                        "-email_match",
                        "-position_match",
                    )
                )

        return queryset


class TeamSearchMixin(ListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        form = TeamSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            if query:
                queryset = (
                    queryset.annotate(
                        name_match=Case(
                            When(name__icontains=query, then=1),
                            default=0,
                        ),
                        member_match=Case(
                            When(members__first_name__icontains=query, then=1),
                            When(members__last_name__icontains=query, then=1),
                            When(members__email__icontains=query, then=1),
                            default=0,
                        ),
                    )
                    .filter(Q(name__icontains=query) | Q(member_match__gte=1))
                    .order_by("-name_match", "-member_match")
                )

        return queryset
