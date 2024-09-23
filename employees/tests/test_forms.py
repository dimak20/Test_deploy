from django.contrib.auth import get_user_model
from django.test import TestCase

from employees.forms import (
    EmployeeInvitationForm,
    EmployeeCreationForm,
    EmployeeAuthenticationForm,
)
from employees.models import Position, Invitation


class EmployeeInvitationFormTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test")
        self.employee = get_user_model().objects.create_user(
            username="testuser", password="Testpass123", position=self.position
        )

    def test_valid_form(self):
        form_data = {"email": "test@example.com", "position": self.position.id}
        form = EmployeeInvitationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_duplicate_email(self):
        Invitation.objects.create(
            email="test@example.com", position=self.position, invited_by=self.employee
        )
        form_data = {"email": "test@example.com", "position": self.position.id}
        form = EmployeeInvitationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class EmployeeCreationFormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "password1": "SecurePassword123",
            "password2": "SecurePassword123",
        }
        form = EmployeeCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "password1": "SecurePassword123",
            "password2": "DifferentPassword123",
        }
        form = EmployeeCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class EmployeeAuthenticationFormTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test")
        self.employee = get_user_model().objects.create_user(
            username="testuser",
            password="Testpass123",
            position=self.position,
            email="test@email.com",
        )

    def test_valid_form(self):
        form_data = {
            "username": "test@email.com",
            "password": "Testpass123",
            "remember_me": True,
        }
        form = EmployeeAuthenticationForm(data=form_data, request=self.client)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form_data = {"username": "testuser", "password": "Testpass123"}
        form = EmployeeAuthenticationForm(data=form_data, request=self.client)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
