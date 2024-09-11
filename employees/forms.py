from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django_select2.forms import Select2MultipleWidget

from employees.models import Invitation, Employee, Team


class EmployeeInvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ["email", "position"]


class EmployeeCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = ["first_name", "last_name", "password1", "password2"]


class EmployeeAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField()


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["position"]


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "members"]
        widgets = {
            "members": Select2MultipleWidget(),
        }
