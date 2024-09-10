import random
import string

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import UpdateView

from employees.forms import EmployeeInvitationForm, EmployeeCreationForm, EmployeeUpdateForm
from employees.models import Invitation, Employee


class EmployeeInvitationView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = EmployeeInvitationForm()
        return render(request, "employees/employee_invite.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = EmployeeInvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.invited_by = request.user
            invitation.save()

            generic_password = "".join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )

            send_mail(
                "You have been invited!",
                f"You have been invited to join. Your login password is: {generic_password}",
                "from@example.com",
                [invitation.email],
                fail_silently=False,
            )

            messages.success(request, "Invitation sent successfully")
            return redirect("/")


class EmployeeRegisterView(View):
    def get(self, request, invitation_id):
        invitation = get_object_or_404(Invitation, pk=invitation_id)
        form = EmployeeCreationForm()
        return render(
            request,
            "employees/employee_register.html",
            {"form": form, "invitation": invitation},
        )

    def post(self, request: HttpRequest, invitation_id) -> HttpResponse:
        invitation = get_object_or_404(Invitation, pk=invitation_id)
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.position = invitation.position
            user.email = invitation.email
            user.username = invitation.email.split("@")[0]
            user.save()
            login(request, user)
            invitation.is_accepted = True
            invitation.save()
            return redirect("/")
        return render(request, "employees/employee_register.html", {"form": form})


class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    template_name = "employees/employee_update.html"
