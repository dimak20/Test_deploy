from django.test import TestCase

from employees.models import Position, Employee, Team


class TestPositionModel(TestCase):
    def test_position_str(self):
        position = Position.objects.create(
            name="Test Position",
        )
        self.assertEqual(str(position), f"{position.name}")


class TestEmployeeModel(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Test Position",
        )
        self.employee = Employee.objects.create_user(
            username="testuser",
            password="Testpass123",
            first_name="First",
            last_name="Last",
            position=self.position,
        )

    def test_employee_str(self):
        self.assertEqual(
            str(self.employee), f"{self.employee.first_name} {self.employee.last_name}"
        )

    def test_employee_slug(self):
        test_slug = (
            f"{self.employee.username}"
            f"-{self.employee.first_name}"
            f"-{self.employee.last_name}"
        ).lower()
        self.assertEqual(self.employee.slug, test_slug)


class TestTeamMode(TestCase):
    def test_team_str(self):
        team = Team.objects.create(name="Test Team")
        self.assertEqual(str(team), f"{team.name}")
