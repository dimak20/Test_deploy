from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from employees.models import Invitation, Employee


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