from django import forms

from tasks.models import Project


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name", "description")


class ProjectSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="",
    )


class TaskSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search.."})
    )
