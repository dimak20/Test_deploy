from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse

from employees.models import Position, Team


class BaseTeamTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test Position")
        self.employee = get_user_model().objects.create_user(
            username="testuser", password="Testpass123", position=self.position
        )


class PublicTeamTests(BaseTeamTests):
    def setUp(self):
        self.team = Team.objects.create(
            name="Test Team",
        )

    def test_team_list_view(self):
        response = self.client.get(reverse("employees:team-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_team_create_view(self):
        response = self.client.get(
            reverse("employees:team-update", kwargs={"slug": self.team.slug})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_team_update_view(self):
        response = self.client.get(
            reverse("employees:team-update", kwargs={"slug": self.team.slug})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_team_delete_view(self):
        response = self.client.get(
            reverse("employees:team-delete", kwargs={"slug": self.team.slug})
        )
        self.assertNotEqual(response.status_code, 200)


class BasePrivateTeamTests(BaseTeamTests):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.employee)


class PrivateTeamListTests(BasePrivateTeamTests):
    TEAM_LIST_URL = reverse("employees:team-list")
    VIEW_PAGINATED_BY = 5

    def setUp(self):
        super().setUp()
        for i in range(6):
            Team.objects.create(name=f"Team {i}")

    def test_team_list_uses_correct_template(self):
        response = self.client.get(self.TEAM_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/teams/team_list.html")

    def test_team_list_pagination(self):
        response = self.client.get(self.TEAM_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(len(response.context["team_list"]), self.VIEW_PAGINATED_BY)

    def test_team_search(self):
        response = self.client.get(self.TEAM_LIST_URL + "?query=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["team_list"]), 1)
        self.assertContains(response, "Team 1")
        self.assertNotContains(response, "Team 2")

    def test_team_list_search_pagination(self):
        response = self.client.get(self.TEAM_LIST_URL + "?query=Team&page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["team_list"]), 5)
        self.assertContains(response, "Team 1")
        self.assertNotContains(response, "Team 5")


class PrivateTeamCreateTests(BasePrivateTeamTests):
    TEAM_CREATE_URL = reverse("employees:team-create")

    def test_create_team_uses_correct_template(self):
        response = self.client.get(self.TEAM_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/teams/team_form.html")

    def test_create_team_post_valid(self):
        form_data = {
            "name": "Test Team",
            "members": [self.employee.id],
        }
        response = self.client.post(self.TEAM_CREATE_URL, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("employees:team-list"))
        self.assertTrue(Team.objects.filter(name="Test Team").exists())


class PrivateTeamUpdateTests(BasePrivateTeamTests):
    def setUp(self):
        super().setUp()
        self.team = Team.objects.create(
            name="Test Team",
        )
        self.TEAM_UPDATE_URL = reverse(
            "employees:team-update", kwargs={"slug": self.team.slug}
        )

    def test_team_update_uses_correct_template(self):
        response = self.client.get(self.TEAM_UPDATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/teams/team_form.html")

    def test_team_update_post(self):
        form_data = {"name": "Updated name"}
        response = self.client.post(self.TEAM_UPDATE_URL, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("employees:team-list"))
        updated_team = Team.objects.get(slug=self.team.slug)
        self.assertEqual(updated_team.name, form_data["name"])


class PrivateTeamDeleteTests(BasePrivateTeamTests):
    def setUp(self):
        super().setUp()
        self.team = Team.objects.create(
            name="Test Project",
        )
        self.TEAM_DELETE_URL = reverse(
            "employees:team-delete", kwargs={"slug": self.team.slug}
        )

    def test_team_delete_uses_correct_template(self):
        response = self.client.get(self.TEAM_DELETE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employees/teams/team_confirm_delete.html")

    def test_team_delete_post(self):
        response = self.client.post(self.TEAM_DELETE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("employees:team-list"))
        deleted_team = Team.objects.filter(slug=self.team.slug)
        self.assertEqual(len(deleted_team), 0)
