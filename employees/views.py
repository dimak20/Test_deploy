import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import UpdateView, DeleteView

from employees.forms import (
    EmployeeInvitationForm,
    EmployeeCreationForm,
    EmployeeUpdateForm,
    EmployeeAuthenticationForm,
)
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
                f"You have been invited to join. Proceed to {reverse('employees:employee-register', args={invitation.slug})}",
                "from@example.com",
                [invitation.email],
                fail_silently=False,
            )

            messages.success(request, "Invitation sent successfully")
            return redirect("/")


class EmployeeRegisterView(View):
    def get(self, request, invitation_slug):
        invitation = get_object_or_404(Invitation, slug=invitation_slug)
        form = EmployeeCreationForm()
        return render(
            request,
            "employees/employee_register.html",
            {"form": form, "invitation": invitation},
        )

    def post(self, request: HttpRequest, invitation_slug) -> HttpResponse:
        invitation = get_object_or_404(Invitation, slug=invitation_slug)
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.position = invitation.position
            user.email = invitation.email
            user.username = invitation.email.split("@")[0]
            user.save()
            user.backend = "employees.backends.EmailBackend"
            login(request, user)
            invitation.is_accepted = True
            invitation.save()
            return redirect("/")
        return render(request, "employees/employee_register.html", {"form": form})


class EmployeeLoginView(LoginView):
    form_class = EmployeeAuthenticationForm
    template_name = "employees/employee_login.html"
    success_url = "/"

    def form_valid(self, form):
        remember_me = form.cleaned_data["remember_me"]

        if remember_me:
            self.request.session.set_expiry(settings.SESSION_COOKIE_AGE)
        else:
            self.request.session.set_expiry(0)

        return super(EmployeeLoginView, self).form_valid(form)


class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    template_name = "employees/employee_update.html"


class EmployeeDeleteView(DeleteView):
    model = Employee
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        employee = self.get_object()

        Invitation.objects.filter(email=employee.email).delete()

        return super(EmployeeDeleteView, self).delete(request, *args, **kwargs)
