from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)
from django_select2.forms import Select2MultipleWidget

from employees.models import Invitation, Team


class EmployeeInvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ["email", "position"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        first_position = self.fields["position"].queryset.first()

        if first_position:
            self.fields["position"].initial = first_position
            self.fields["position"].empty_label = None

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Invitation.objects.filter(email=email).exists():
            raise forms.ValidationError("An invitation with this email already exists.")
        return email


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
        fields = ("position",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["position"].widget.attrs.update(
            {"class": "form-control form-control-lg"}
        )
        self.fields["position"].empty_label = None


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "members"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Name"}),
            "members": Select2MultipleWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get("class"):
                field.widget.attrs["class"] += " form-control form-control-lg"
            else:
                field.widget.attrs.update({"class": "form-control form-control-lg"})

            if self.errors.get(field_name):
                field.widget.attrs["class"] += " is-invalid"


class InvitationSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="",
    )


class EmployeeSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="",
    )


class TeamSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="",
    )
