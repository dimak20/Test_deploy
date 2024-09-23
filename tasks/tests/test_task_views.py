from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from employees.models import Position
from tasks.models import Project, TaskType, Task


class BaseTasksTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test Position")
        self.employee = get_user_model().objects.create_user(
            username="testuser", password="Testpass123", position=self.position
        )


class PublicTasksTests(BaseTasksTests):
    def setUp(self):
        self.project = Project.objects.create(
            name="Test Project",
        )
        self.task_type = TaskType.objects.create(name="Test Task Type")
        self.task = Task.objects.create(
            name="Test Task",
            project=self.project,
            task_type=self.task_type,
            deadline=timezone.now(),
        )

    def test_task_create(self):
        response = self.client.get(
            reverse("tasks:task-create", kwargs={"project_slug": self.project.slug})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_task_detail(self):
        response = self.client.get(
            reverse("tasks:task-detail", kwargs={"slug": self.task.slug})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_task_update(self):
        response = self.client.get(
            reverse("tasks:task-update", kwargs={"slug": self.task.slug})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_task_delete(self):
        response = self.client.get(
            reverse("tasks:task-delete", kwargs={"slug": self.task.slug})
        )
        self.assertNotEqual(response.status_code, 200)


class BasePrivateProjectTests(BaseTasksTests):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.employee)
        self.project = Project.objects.create(
            name="Test Project",
        )
        self.task_type = TaskType.objects.create(name="Test Task Type")


class PrivateTaskCreateTests(BasePrivateProjectTests):
    def setUp(self):
        super().setUp()
        self.TASK_CREATE_URL = reverse(
            "tasks:task-create", kwargs={"project_slug": self.project.slug}
        )

    def test_create_task_uses_correct_template(self):
        response = self.client.get(self.TASK_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_form.html")

    def test_create_task_post_valid(self):
        form_data = {
            "name": "Test Task",
            "project": self.project.id,
            "priority": 1,
            "task_type": self.task_type.id,
            "deadline": timezone.now() + timedelta(days=1),
        }
        response = self.client.post(self.TASK_CREATE_URL, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("tasks:project-detail", kwargs={"slug": self.project.slug}),
        )
        self.assertTrue(Task.objects.filter(name="Test Task").exists())


class PrivateDetailViewTests(BasePrivateProjectTests):
    def setUp(self):
        super().setUp()
        self.task = Task.objects.create(
            name="Test Task",
            project=self.project,
            task_type=self.task_type,
            deadline=timezone.now(),
        )
        self.TASK_DETAIL_URL = reverse(
            "tasks:task-detail", kwargs={"slug": self.task.slug}
        )

    def test_task_detail_uses_correct_template(self):
        response = self.client.get(self.TASK_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_detail.html")
        self.assertContains(response, self.task.name)

    def test_task_detail_post_complete_task(self):
        form_data = {"action": "complete"}
        response = self.client.post(self.TASK_DETAIL_URL, data=form_data)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
        self.assertEqual(self.task.completed_by, self.employee)
        self.assertRedirects(
            response, reverse("tasks:task-detail", kwargs={"slug": self.task.slug})
        )

    def test_task_detail_post_reopen_task(self):
        self.task.is_completed = True
        self.task.completed_by = self.employee
        self.task.save()

        form_data = {"action": "open"}
        response = self.client.post(self.TASK_DETAIL_URL, data=form_data)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)
        self.assertEqual(self.task.completed_by, None)
        self.assertRedirects(
            response, reverse("tasks:task-detail", kwargs={"slug": self.task.slug})
        )


class PrivateTaskUpdateTests(BasePrivateProjectTests):
    def setUp(self):
        super().setUp()
        self.task = Task.objects.create(
            name="Test Task",
            project=self.project,
            task_type=self.task_type,
            deadline=timezone.now(),
        )
        self.TASK_UPDATE_URL = reverse(
            "tasks:task-update", kwargs={"slug": self.task.slug}
        )

    def test_task_update_uses_correct_template(self):
        response = self.client.get(self.TASK_UPDATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_form.html")

    def test_task_update_post_valid(self):
        form_data = {
            "name": "Updated Task",
            "project": self.project.id,
            "priority": 1,
            "task_type": self.task_type.id,
            "deadline": timezone.now() + timedelta(days=1),
        }
        response = self.client.post(self.TASK_UPDATE_URL, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("tasks:task-detail", kwargs={"slug": self.task.slug})
        )
        updated_task = Task.objects.get(slug=self.task.slug)
        self.assertEqual(updated_task.name, form_data["name"])


class PrivateTaskDeleteTests(BasePrivateProjectTests):
    def setUp(self):
        super().setUp()
        self.task = Task.objects.create(
            name="Test Task",
            project=self.project,
            task_type=self.task_type,
            deadline=timezone.now(),
        )
        self.TASK_DELETE_URL = reverse(
            "tasks:task-delete", kwargs={"slug": self.task.slug}
        )

    def test_task_delete_uses_correct_template(self):
        response = self.client.get(self.TASK_DELETE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_confirm_delete.html")

    def test_task_delete_post_valid(self):
        response = self.client.post(self.TASK_DELETE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("tasks:project-detail", kwargs={"slug": self.project.slug}),
        )
        deleted_task = Task.objects.filter(slug=self.task.slug)
        self.assertEqual(len(deleted_task), 0)
