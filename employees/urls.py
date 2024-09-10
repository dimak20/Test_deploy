from django.urls import path

from employees.views import EmployeeInvitationView, EmployeeRegisterView, EmployeeUpdateView

app_name = "employees"

urlpatterns = [
    path("employees/invite/", EmployeeInvitationView.as_view(), name="employee-invite"),
    path("employees/register/<int:invitation_id>/", EmployeeRegisterView.as_view(), name="employee-register"),
    path("employees/<int:pk>/update/", EmployeeUpdateView.as_view(), name="employee-update"),
]