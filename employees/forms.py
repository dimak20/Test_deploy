from django import forms

from employees.models import Invitation


class EmployeeInvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ["email", "position"]
