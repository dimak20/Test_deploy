from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    position = models.ForeignKey("Position", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Invitation(models.Model):
    email = models.EmailField(unique=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)


class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(get_user_model(), related_name='teams')
