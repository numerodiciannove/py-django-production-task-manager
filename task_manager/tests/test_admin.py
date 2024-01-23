from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from task_manager.models import Project, TaskType, Task, Position, Worker, Team


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            username="admin_Zina", email="admin@example.com",
            password="Gh_uIhg/#4"
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(name="Test Position")
        self.task_type = TaskType.objects.create(name="Test Type")
        self.project = Project.objects.create(name="Test Project")
        self.worker = Worker.objects.create(
            username="test_user",
            first_name="John",
            last_name="Doe",
            position=self.position,
            phone_number="+380951911919",
            country="UA",
        )
        self.team = Team.objects.create(name="Test Team")

    def test_task_admin(self):
        task_data = {
            "name": "Test Task",
            "project": self.project.id,
            "priority": "urgent",
        }
        response = self.client.post(
            reverse("admin:task_manager_task_add"), task_data, follow=True
        )
        self.assertEqual(response.status_code, 200)

        task = Task.objects.create(name="Test Task")

        response = self.client.get(
            reverse("admin:task_manager_task_change", args=[task.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_worker_admin(self):
        worker_data = {
            "username": "test_user_2",
            "first_name": "Jane",
            "last_name": "Doe",
            "position": self.position,
            "phone_number": "+987654321",
            "country": "CA",
        }
        response = self.client.post(
            reverse("admin:task_manager_worker_add"), worker_data, follow=True
        )
        self.assertEqual(response.status_code, 200)

        worker = Worker.objects.create(**worker_data)

        response = self.client.get(
            reverse("admin:task_manager_worker_change", args=[worker.id])
        )
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "test_user_2")
        self.assertContains(response, "Jane")
        self.assertContains(response, "Doe")

    def test_project_admin(self):
        project = Project.objects.create(name="Test Project 2")

        response = self.client.get(
            reverse("admin:task_manager_project_change", args=[project.id])
        )
        self.assertEqual(response.status_code, 200)
