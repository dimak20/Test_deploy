from django.conf import settings
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField

from employees.models import Team


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("1", "Urgent"),
        ("2", "High"),
        ("3", "Medium"),
        ("4", "Low"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="tasks"
    )
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL
    )
    priority = models.CharField(max_length=100, choices=PRIORITY_CHOICES, blank=False, null=False)
    task_type = models.ForeignKey("TaskType", on_delete=models.RESTRICT)
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="tasks", blank=True
    )
    tags = models.ManyToManyField("TaskTag", blank=True)
    slug = AutoSlugField(populate_from=["name"], unique=True)

    class Meta:
        ordering = ("is_completed", "priority", "-deadline", "name")

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TaskTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    teams = models.ManyToManyField(Team, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from=["name"], unique=True)

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tasks:project-detail", kwargs={"slug": self.slug})
