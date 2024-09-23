from django.test import TestCase
from django.utils import timezone

from tasks.models import Task, Project, TaskType, TaskTag


class BaseTasksModelsTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Test Project",
        )
        self.task_type = TaskType.objects.create(
            name="Test Task Type",
        )
        self.task = Task.objects.create(
            name="Test Task",
            project=self.project,
            task_type=self.task_type,
            deadline=timezone.now(),
        )


class TestTaskModel(BaseTasksModelsTests):
    def test_task_str(self):
        self.assertEqual(str(self.task), self.task.name)


class TestTaskTypeModel(BaseTasksModelsTests):
    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), self.task_type.name)


class TestTaskTagModel(BaseTasksModelsTests):
    def test_task_tag_str(self):
        task_tag = TaskTag.objects.create(
            name="Test Task Tag",
        )
        self.assertEqual(str(task_tag), task_tag.name)


class TestProjectModel(BaseTasksModelsTests):
    def test_project_str(self):
        self.assertEqual(str(self.project), self.project.name)
