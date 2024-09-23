from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse

from employees.models import Position, Invitation


class PublicInvitationTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test Position")

    def test_get_employee_invitation_login_required(self):
        response = self.client.get(reverse("employees:employee-invite"))
        self.assertNotEqual(response.status_code, 200)

    def test_post_employee_invitation_login_required(self):
        form_data = {
            "email": "test@email.com",
            "position_id": self.position.id,
        }
        response = self.client.post(
            reverse("employees:employee-invite"), data=form_data
        )
        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(Invitation.objects.filter(email=form_data["email"]).exists())

    def test_invitation_list_login_required(self):
        response = self.client.get(reverse("employees:invitation-list"))
        self.assertNotEqual(response.status_code, 200)


class BasePrivateInvitationTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test Position")
        self.employee = get_user_model().objects.create_user(
            username="testuser", password="Testpass123", position=self.position
        )
        self.client.force_login(self.employee)


class PrivateEmployeeInvitationTests(BasePrivateInvitationTests):
    def setUp(self):
        super().setUp()

    def test_get_employee_invitation_view(self):
        response = self.client.get(reverse("employees:employee-invite"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/employee_invite.html")

    def test_post_employee_invitation_view(self):
        form_data = {
            "email": "test@email.com",
            "position": self.position.id,
        }
        response = self.client.post(
            reverse("employees:employee-invite"), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("employees:invitation-list"))
        self.assertTrue(Invitation.objects.filter(email=form_data["email"]).exists())


class PrivateInvitationListTests(BasePrivateInvitationTests):
    INVITATION_LIST_URL = reverse("employees:invitation-list")
    VIEW_PAGINATED_BY = 5

    def setUp(self):
        super().setUp()
        for i in range(6):
            Invitation.objects.create(
                email=f"test{i}@email.com",
                position=self.position,
                invited_by=self.employee,
            )

    def test_invitation_list_template(self):
        response = self.client.get(self.INVITATION_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/invitations/invitation_list.html")

    def test_invitation_list_pagination(self):
        response = self.client.get(self.INVITATION_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(
            len(response.context["invitation_list"]), self.VIEW_PAGINATED_BY
        )

    def test_invitation_list_search(self):
        response = self.client.get(self.INVITATION_LIST_URL + "?query=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["invitation_list"]), 1)
        self.assertContains(response, "test1@email.com")
        self.assertNotContains(response, "test2@email.com")

    def test_invitation_list_search_pagination(self):
        response = self.client.get(self.INVITATION_LIST_URL + "?query=test&page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["invitation_list"]), 5)
        self.assertContains(response, "test1@email.com")
        self.assertNotContains(response, "test5@email.com")
