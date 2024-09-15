from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django_select2.forms import Select2MultipleWidget

from employees.models import Invitation, Team


class EmployeeInvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ["email", "position"]


class EmployeeCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["first_name", "last_name", "password1", "password2"]


class EmployeeAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)

    class Meta(AuthenticationForm):
        model = get_user_model()
        fields = ["email", "password", "remember_me"]


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["position"]


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "members"]
        widgets = {
            "members": Select2MultipleWidget(),
        }
