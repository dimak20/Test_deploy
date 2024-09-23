from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.fields import AutoSlugField


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    position = models.ForeignKey("Position", on_delete=models.RESTRICT)
    slug = AutoSlugField(
        populate_from=["username", "first_name", "last_name"], unique=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="teams", blank=True
    )
    slug = AutoSlugField(populate_from=["name"], unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name
