from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse

from employees.models import Position, Invitation


class BaseEmployeeTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test Position")
        self.employee = get_user_model().objects.create_user(
            username="testuser", password="Testpass123", position=self.position
        )


class PublicEmployeeTests(BaseEmployeeTests):
    def test_employee_list_login_required(self):
        response = self.client.get(reverse("employees:employee-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_employee_update_login_required(self):
        response = self.client.get(
            reverse("employees:employee-update", kwargs={"slug": self.employee.slug})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_employee_delete_login_required(self):
        response = self.client.get(
            reverse("employees:employee-delete", kwargs={"slug": self.employee.slug})
        )
        self.assertNotEqual(response.status_code, 200)


class BasePrivateEmployeeTests(BaseEmployeeTests):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.employee)


class PrivateEmployeeListTests(BasePrivateEmployeeTests):
    EMPLOYEE_LIST_URL = reverse("employees:employee-list")
    VIEW_PAGINATED_BY = 5

    def setUp(self):
        super().setUp()
        for i in range(6):
            get_user_model().objects.create_user(
                username=f"testuser{i}",
                password=f"Testpass{i}",
                position=self.position,
                first_name=f"First{i}",
                last_name=f"Last{i}",
                email=f"test{i}@email.com",
            )

    def test_employee_list_uses_correct_template(self):
        response = self.client.get(self.EMPLOYEE_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/employee_list.html")

    def test_employee_list_pagination(self):
        response = self.client.get(self.EMPLOYEE_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(len(response.context["employee_list"]), self.VIEW_PAGINATED_BY)

    def test_employee_search(self):
        response = self.client.get(self.EMPLOYEE_LIST_URL + "?query=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["employee_list"]), 1)
        self.assertContains(response, "test1@email.com")
        self.assertNotContains(response, "test2@email.com")

    def test_employee_list_search_pagination(self):
        response = self.client.get(self.EMPLOYEE_LIST_URL + "?query=test&page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["employee_list"]), 5)
        self.assertContains(response, "test1@email.com")
        self.assertNotContains(response, "test5@email.com")


class PrivateEmployeeUpdateTests(BasePrivateEmployeeTests):
    def setUp(self):
        super().setUp()
        self.EMPLOYEE_UPDATE_URL = reverse(
            "employees:employee-update", kwargs={"slug": self.employee.slug}
        )

    def test_employee_update_uses_correct_template(self):
        response = self.client.get(self.EMPLOYEE_UPDATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/employee_update.html")

    def test_employee_update_post(self):
        position = Position.objects.create(name="Another Position")
        form = {
            "position": position.id,
        }
        response = self.client.post(self.EMPLOYEE_UPDATE_URL, data=form)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("employees:employee-list"))
        updated_employee = get_user_model().objects.get(slug=self.employee.slug)
        self.assertEqual(updated_employee.position, position)


class PrivateEmployeeDeleteTests(BasePrivateEmployeeTests):
    def setUp(self):
        super().setUp()
        self.employee_to_delete = get_user_model().objects.create_user(
            username="deleteuser", password="Testpass", position=self.position
        )
        self.EMPLOYEE_DELETE_URL = reverse(
            "employees:employee-delete", kwargs={"slug": self.employee_to_delete.slug}
        )

    def test_employee_delete_uses_correct_template(self):
        response = self.client.get(self.EMPLOYEE_DELETE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/employee_confirm_delete.html")

    def test_employee_delete_post(self):
        response = self.client.post(self.EMPLOYEE_DELETE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("employees:employee-list"))
        deleted_employees = get_user_model().objects.filter(
            slug=self.employee_to_delete.slug
        )
        self.assertEqual(len(deleted_employees), 0)


class EmployeeRegisterTests(BaseEmployeeTests):
    def setUp(self):
        super().setUp()
        self.position = Position.objects.create(name="Test Position")
        self.invitation = Invitation.objects.create(
            email="test@email.com", position=self.position, invited_by=self.employee
        )

    def test_employee_register_view_uses_correct_template(self):
        response = self.client.get(
            reverse(
                "employees:employee-register",
                kwargs={"invitation_slug": self.invitation.slug},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/employee_register.html")

    def test_employee_register_view_post_valid(self):
        post_data = {
            "first_name": "John",
            "last_name": "Doe",
            "password1": "Testpass123",
            "password2": "Testpass123",
        }
        response = self.client.post(
            reverse(
                "employees:employee-register",
                kwargs={"invitation_slug": self.invitation.slug},
            ),
            data=post_data,
        )
        self.assertRedirects(response, reverse("tasks:dashboard"))
        employee = get_user_model().objects.get(email=self.invitation.email)
        self.assertTrue(employee.is_authenticated)

    def test_employee_register_view_post_invalid(self):
        post_data = {
            "username": "register",
            "password1": "password123",
            "password2": "wrongpassword",
        }
        response = self.client.post(
            reverse(
                "employees:employee-register",
                kwargs={"invitation_slug": self.invitation.slug},
            ),
            data=post_data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/employee_register.html")
        self.assertFalse(
            get_user_model().objects.filter(email=self.invitation.email).exists()
        )


class EmployeeLoginTests(BaseEmployeeTests):
    def test_employee_login_uses_correct_template(self):
        response = self.client.get(reverse("employees:employee-login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/employee_login.html")

    def test_employee_login_view_post_valid(self):
        user = get_user_model().objects.create_user(
            username="testlogin",
            email="testuser@example.com",
            password="password123",
            position=self.position,
        )
        post_data = {
            "username": "testuser@example.com",
            "password": "password123",
            "remember_me": True,
        }
        response = self.client.post(reverse("employees:employee-login"), data=post_data)
        self.assertRedirects(response, reverse("tasks:dashboard"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_employee_login_view_post_invalid(self):
        post_data = {
            "username": "invalid@example.com",
            "password": "wrongpassword",
        }
        response = self.client.post(reverse("employees:employee-login"), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/employee_login.html")


class EmployeeLogoutTests(BaseEmployeeTests):
    def test_employee_logout_view(self):
        self.client.force_login(self.employee)
        response = self.client.post(reverse("employees:employee-logout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/employee_logout.html")
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class EmployeePasswordResetTests(BaseEmployeeTests):
    def test_employee_password_reset_view(self):
        response = self.client.get(reverse("employees:password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "employees/reset_password/password_reset.html"
        )

    def test_employee_password_reset_complete_view(self):
        response = self.client.get(reverse("employees:password_reset_complete"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "employees/reset_password/password_reset_complete.html"
        )
