from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetCompleteView, LogoutView,
)
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView, ListView, CreateView

from employees.forms import (
    EmployeeInvitationForm,
    EmployeeCreationForm,
    EmployeeUpdateForm,
    EmployeeAuthenticationForm,
    TeamForm,
)
from employees.mixins import InvitationSearchMixin, EmployeeSearchMixin, TeamSearchMixin
from employees.models import Invitation, Team


class EmployeeInvitationView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = EmployeeInvitationForm()
        return render(request, "employees/employee_invite.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = EmployeeInvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.invited_by = request.user
            invitation.save()

            send_mail(
                "You have been invited!",
                f"{request.user} has invited you to join. Proceed to {reverse('employees:employee-register', args={invitation.slug})}",
                "from@example.com",
                [invitation.email],
                fail_silently=False,
            )

            messages.success(request, "Invitation sent successfully")
            return redirect(reverse("employees:invitation-list"))
        else:
            return render(request, "employees/employee_invite.html", {"form": form})


class InvitationListView(InvitationSearchMixin, ListView):
    model = Invitation
    template_name = "employees/invitations/invitation_list.html"
    paginate_by = 5


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

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        remember_me = form.cleaned_data["remember_me"]

        if remember_me:
            self.request.session.set_expiry(settings.SESSION_COOKIE_AGE)
        else:
            self.request.session.set_expiry(0)

        return super(EmployeeLoginView, self).form_valid(form)

    def get_success_url(self):
        if self.request.GET.get("next"):
            return self.request.GET.get("next")
        return reverse_lazy("tasks:dashboard")


class EmployeeLogoutView(LogoutView):
    template_name = "employees/employee_logout.html"
    success_url = reverse_lazy("tasks:dashboard")


class EmployeePasswordResetView(PasswordResetView):
    template_name = "employees/reset_password/password_reset.html"
    email_template_name = "employees/password_reset_email.html"
    success_url = reverse_lazy("employees:password_reset_done")


class EmployeePasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "employees/reset_password/password_reset_complete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = reverse("employees:employee-login")
        return context


class EmployeeListView(LoginRequiredMixin, EmployeeSearchMixin, ListView):
    model = get_user_model()
    template_name = "employees/employee_list.html"
    paginate_by = 5


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = EmployeeUpdateForm
    template_name = "employees/employee_update.html"
    success_url = reverse_lazy("employees:employee-list")


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("employees:employee-list")

    def delete(self, request, *args, **kwargs):
        employee = self.get_object()

        Invitation.objects.filter(email=employee.email).delete()

        return super(EmployeeDeleteView, self).delete(request, *args, **kwargs)


class TeamListView(LoginRequiredMixin, TeamSearchMixin, ListView):
    model = Team
    paginate_by = 5


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = "employees/team_form.html"
    success_url = "/"


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = "employees/team_form.html"
    success_url = reverse_lazy("tasks:team-list")



class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    success_url = reverse_lazy("tasks:team-list")
