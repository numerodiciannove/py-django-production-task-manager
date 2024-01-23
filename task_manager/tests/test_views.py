from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from task_manager.models import Project, Task, Worker, Team, Position


class TaskManagerViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.position = Position.objects.create(name="Test Position")
        self.worker = Worker.objects.create(
            username="test_worker",
            first_name="John",
            last_name="Doe",
            position=self.position,
            phone_number="+123456789",
            country="US",
        )
        self.team = Team.objects.create(name="Test Team")
        self.project = Project.objects.create(name="Test Project")
        self.project.teams.set([self.team])
        self.task = Task.objects.create(name="Test Task", project=self.project)

    def assert_view_status_code(self, view_name, *args):
        url = reverse(view_name, args=args)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_task_list_view(self):
        self.assert_view_status_code("task_manager:tasks-list")

    def test_task_detail_view(self):
        self.assert_view_status_code("task_manager:task-detail", self.task.id)

    def test_task_create_view(self):
        self.assert_view_status_code("task_manager:task-create")

    def test_task_update_view(self):
        self.assert_view_status_code("task_manager:task-update", self.task.id)

    def test_task_delete_view(self):
        self.assert_view_status_code("task_manager:task-delete", self.task.id)

    def test_worker_list_view(self):
        self.assert_view_status_code("task_manager:workers-list")

    def test_worker_detail_view(self):
        self.assert_view_status_code("task_manager:worker-detail",
                                     self.worker.id)

    def test_worker_create_view(self):
        self.assert_view_status_code("task_manager:worker-create")

    def test_worker_update_view(self):
        self.assert_view_status_code("task_manager:worker-update",
                                     self.worker.id)

    def test_worker_delete_view(self):
        self.assert_view_status_code("task_manager:worker-delete",
                                     self.worker.id)

    def test_team_list_view(self):
        self.assert_view_status_code("task_manager:teams-list")

    def test_team_detail_view(self):
        self.assert_view_status_code("task_manager:team-detail", self.team.id)

    def test_team_create_view(self):
        self.assert_view_status_code("task_manager:team-create")

    def test_team_update_view(self):
        self.assert_view_status_code("task_manager:team-update", self.team.id)

    def test_team_delete_view(self):
        self.assert_view_status_code("task_manager:team-delete", self.team.id)

    def test_position_list_view(self):
        self.assert_view_status_code("task_manager:positions-list")

    def test_position_create_view(self):
        self.assert_view_status_code("task_manager:position-create")

    def test_position_update_view(self):
        self.assert_view_status_code("task_manager:position-update",
                                     self.position.id)

    def test_position_delete_view(self):
        self.assert_view_status_code("task_manager:position-delete",
                                     self.position.id)
