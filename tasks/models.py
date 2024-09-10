from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField

from employees.models import Team


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("urgent", "Urgent"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="tasks"
    )
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=100, choices=PRIORITY_CHOICES)
    task_type = models.ForeignKey("TaskType", on_delete=models.RESTRICT)
    assignees = models.ManyToManyField(get_user_model(), related_name="tasks")
    tags = models.ManyToManyField("TaskTag")

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
    teams = models.ManyToManyField(Team)
    start_date = models.DateField(auto_now_add=True)
    slug = AutoSlugField(populate_from=["name"], unique=True, auto_created=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)

        start_month = self.start_date.strftime('%m-%Y')
        if not self.slug.endswith(start_month):
            self.slug = f"{self.slug}-{start_month}"
            self.save()

    def get_absolute_url(self):
        return reverse("tasks:project-detail", kwargs={"slug": self.slug})
