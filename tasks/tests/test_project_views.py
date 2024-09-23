from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from employees.models import Position, Team
from tasks.models import Project, Task, TaskType


class BaseProjectTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test Position")
        self.employee = get_user_model().objects.create_user(
            username="testuser", password="Testpass123", position=self.position
        )


class PublicProjectTests(BaseProjectTests):
    def setUp(self):
        self.project = Project.objects.create(
            name="Test Project",
        )

    def test_project_list(self):
        response = self.client.get(reverse("tasks:project-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_project_detail(self):
        response = self.client.get(
            reverse("tasks:project-detail", kwargs={"slug": self.project.slug})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_project_create(self):
        response = self.client.get(reverse("tasks:project-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_project_update(self):
        response = self.client.get(
            reverse("tasks:project-update", kwargs={"slug": self.project.slug})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_project_delete(self):
        response = self.client.get(
            reverse("tasks:project-delete", kwargs={"slug": self.project.slug})
        )
        self.assertNotEqual(response.status_code, 200)


class BasePrivateProjectTests(BaseProjectTests):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.employee)


class PrivateProjectListTests(BasePrivateProjectTests):
    PROJECT_LIST_URL = reverse("tasks:project-list")
    VIEW_PAGINATED_BY = 5

    def setUp(self):
        super().setUp()
        for i in range(6):
            Project.objects.create(name=f"Test Project {i}")

    def test_project_list_uses_correct_template(self):
        response = self.client.get(self.PROJECT_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/projects/project_list.html")

    def test_project_list_pagination(self):
        response = self.client.get(self.PROJECT_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(len(response.context["project_list"]), self.VIEW_PAGINATED_BY)

    def test_project_search(self):
        response = self.client.get(self.PROJECT_LIST_URL + "?query=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["project_list"]), 1)
        self.assertContains(response, "Test Project 1")
        self.assertNotContains(response, "Test Project 2")

    def test_project_list_search_pagination(self):
        response = self.client.get(self.PROJECT_LIST_URL + "?query=Test&page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["project_list"]), 5)
        self.assertContains(response, "Test Project 1")
        self.assertNotContains(response, "Test Project 5")


class PrivateProjectDetailTests(BasePrivateProjectTests):
    def setUp(self):
        super().setUp()
        self.project = Project.objects.create(
            name="Test Project",
        )
        self.PROJECT_DETAIL_URL = reverse(
            "tasks:project-detail", kwargs={"slug": self.project.slug}
        )

        task_type = TaskType.objects.create(name="Test Type")
        for i in range(6):
            self.task = Task.objects.create(
                name=f"Test Task {i}",
                task_type=task_type,
                project=self.project,
                deadline=timezone.now(),
            )

    def test_project_detail_uses_correct_template(self):
        response = self.client.get(self.PROJECT_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/projects/project_detail.html")

    def test_project_detail_has_project_tasks(self):
        response = self.client.get(self.PROJECT_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("tasks" in response.context)
        self.assertEqual(len(response.context["tasks"]), 6)

    def test_project_detail_task_search(self):
        response = self.client.get(self.PROJECT_DETAIL_URL + "?query=1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("tasks" in response.context)
        self.assertEqual(len(response.context["tasks"]), 1)


class PrivateProjectCreateView(BasePrivateProjectTests):
    PROJECT_CREATE_URL = reverse("tasks:project-create")

    def test_create_project_uses_correct_template(self):
        response = self.client.get(self.PROJECT_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/projects/project_form.html")

    def test_create_project_post_valid(self):
        form_data = {
            "name": "Test Project",
            "description": "Test Description",
        }
        response = self.client.post(self.PROJECT_CREATE_URL, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:project-list"))
        self.assertTrue(Project.objects.filter(name="Test Project").exists())


class PrivateProjectUpdateTests(BasePrivateProjectTests):
    def setUp(self):
        super().setUp()
        self.project = Project.objects.create(
            name="Test Project",
        )
        self.PROJECT_UPDATE_URL = reverse(
            "tasks:project-update", kwargs={"slug": self.project.slug}
        )

    def test_project_update_uses_correct_template(self):
        response = self.client.get(self.PROJECT_UPDATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/projects/project_form.html")

    def test_project_update_post(self):
        form_data = {"name": "Updated name"}
        response = self.client.post(self.PROJECT_UPDATE_URL, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:project-list"))
        updated_project = Project.objects.get(slug=self.project.slug)
        self.assertEqual(updated_project.name, form_data["name"])


class PrivateProjectDeleteTests(BasePrivateProjectTests):
    def setUp(self):
        super().setUp()
        self.project = Project.objects.create(
            name="Test Project",
        )
        self.PROJECT_DELETE_URL = reverse(
            "tasks:project-delete", kwargs={"slug": self.project.slug}
        )

    def test_project_delete_uses_correct_template(self):
        response = self.client.get(self.PROJECT_DELETE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/projects/project_confirm_delete.html")

    def test_project_delete_post(self):
        response = self.client.post(self.PROJECT_DELETE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:project-list"))
        deleted_project = Project.objects.filter(slug=self.project.slug)
        self.assertEqual(len(deleted_project), 0)
