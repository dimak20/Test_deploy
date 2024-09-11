from django.urls import path

from employees.views import (
    EmployeeInvitationView,
    EmployeeRegisterView,
    EmployeeLoginView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    TeamListView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView,
)

app_name = "employees"

urlpatterns = [
    path("employees/invite/", EmployeeInvitationView.as_view(), name="employee-invite"),
    path(
        "employees/register/<slug:invitation_slug>/",
        EmployeeRegisterView.as_view(),
        name="employee-register",
    ),
    path("employees/login/", EmployeeLoginView.as_view(), name="employee-login"),
    path(
        "employees/<slug:slug>/update/",
        EmployeeUpdateView.as_view(),
        name="employee-update",
    ),
    path(
        "employees/<slug:slug>/delete/",
        EmployeeDeleteView.as_view(),
        name="employee-delete",
    ),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("teams/create/", TeamCreateView.as_view(), name="team-create"),
    path("teams/<slug:slug>/update", TeamUpdateView.as_view(), name="team-update"),
    path("teams/<slug:slug>/delete", TeamDeleteView.as_view(), name="team-delete"),
]
