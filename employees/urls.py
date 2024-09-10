from django.urls import path

from employees.views import EmployeeInvitationView


app_name = "employees"

urlpatterns = [
    path("employees/invite/", EmployeeInvitationView.as_view(), name="employee-invite"),
]