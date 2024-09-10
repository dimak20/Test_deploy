import random
import string

from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from employees.forms import EmployeeInvitationForm


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
