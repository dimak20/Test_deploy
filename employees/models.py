from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    position = models.ForeignKey("Position", on_delete=models.CASCADE)
    slug = AutoSlugField(
        populate_from=["username", "first_name", "last_name"],
        unique=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("employees:detail", kwargs={"slug": self.slug})


class Invitation(models.Model):
    email = models.EmailField(unique=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from=["position", "created_at"], unique=True)

    class Meta:
        ordering = ("-created_at",)


class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(get_user_model(), related_name="teams")
    slug = AutoSlugField(populate_from=["name"], unique=True)

    def __str__(self):
        return self.name
