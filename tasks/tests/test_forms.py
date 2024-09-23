from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from tasks.forms import TaskForm
from tasks.models import TaskType


class TaskFormTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(
            name="Test Task Type",
        )

    def test_task_form_valid(self):
        form = TaskForm(
            data={
                "name": "Task 1",
                "description": "Task description",
                "deadline": timezone.now() + timedelta(days=1),
                "priority": 1,
                "task_type": self.task_type.id,
            }
        )
        self.assertTrue(form.is_valid())

    def test_task_form_invalid(self):
        form = TaskForm(
            data={
                "name": "Task 1",
                "description": "Task description",
                "deadline": timezone.now() - timedelta(days=1),
                "priority": 1,
                "task_type": self.task_type.id,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)
