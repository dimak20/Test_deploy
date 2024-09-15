from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views


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
    EmployeePasswordResetView,
    EmployeePasswordResetCompleteView
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
        "employees/password_reset/",
        EmployeePasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "employees/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="employees/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "employees/password_reset/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="employees/password_reset_confirm.html",
            success_url=reverse_lazy("employees:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "employees/password_reset/complete/",
        EmployeePasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
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
    # path("employees/", include("django.contrib.auth.urls"))
]
