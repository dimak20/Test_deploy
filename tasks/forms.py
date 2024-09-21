from django import forms
from django.utils import timezone
from django_select2.forms import Select2MultipleWidget

from tasks.models import Project, Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name", "description", "teams")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Title"}),
            "description": forms.Textarea(attrs={"placeholder": "Description"}),
            "teams": Select2MultipleWidget(),
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


class ProjectSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="",
    )


class TaskForm(forms.ModelForm):
    priority = forms.ChoiceField(choices=Task.PRIORITY_CHOICES)

    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "assignees",
            "tags",
        )
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Title"}),
            "description": forms.Textarea(attrs={"placeholder": "Description"}),
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local", "title": "Deadline"}
            ),
            "assignees": Select2MultipleWidget(),
            "tags": Select2MultipleWidget(),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < timezone.now():
            raise forms.ValidationError("Deadline must be in the future")
        return deadline

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get("class"):
                field.widget.attrs["class"] += " form-control form-control-lg"
            else:
                field.widget.attrs.update({"class": "form-control form-control-lg"})

            if field_name in ("priority", "task_type"):
                field.widget.attrs["class"] += " form-select"

            if self.errors.get(field_name):
                field.widget.attrs["class"] += " is-invalid"

        self.fields["priority"].initial = "urgent"
        self.fields["priority"].empty_label = None

        first_task_type = self.fields["task_type"].queryset.first()
        if first_task_type:
            self.fields["task_type"].initial = first_task_type
            self.fields["task_type"].empty_label = None


class TaskSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search.."}),
    )
