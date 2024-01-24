from django.test import TestCase

from task_manager.models import Project, TaskType, Task, Position, Worker, Team


class ProjectModelTest(TestCase):
    def test_create_project(self):
        project = Project.objects.create(
            name="Test Project", description="This is a test project",
            budget=1000
        )
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.description, "This is a test project")
        self.assertEqual(project.budget, 1000)

    def test_project_str_method(self):
        project = Project.objects.create(name="Test Project")
        self.assertEqual(str(project), "Test Project")


class TaskTypeModelTest(TestCase):
    def test_create_task_type(self):
        task_type = TaskType.objects.create(name="Test Type")
        self.assertEqual(task_type.name, "Test Type")

    def test_task_type_str_method(self):
        task_type = TaskType.objects.create(name="Test Type")
        self.assertEqual(str(task_type), "Test Type")


class TaskModelTest(TestCase):
    def setUp(self):
        project = Project.objects.create(name="Test Project")
        task_type = TaskType.objects.create(name="Test Type")
        self.task = Task.objects.create(
            name="Test Task", project=project, priority="urgent"
        )
        self.task.task_type.add(task_type)

    def test_create_task(self):
        self.assertEqual(self.task.name, "Test Task")
        self.assertEqual(self.task.project.name, "Test Project")
        self.assertEqual(self.task.priority, "urgent")
        self.assertEqual(self.task.task_type.first().name, "Test Type")

    def test_task_str_method(self):
        self.assertEqual(str(self.task), "Test Task")


class PositionModelTest(TestCase):
    def test_create_position(self):
        position = Position.objects.create(name="Test Position")
        self.assertEqual(position.name, "Test Position")

    def test_position_str_method(self):
        position = Position.objects.create(name="Test Position")
        self.assertEqual(str(position), "Test Position")


class WorkerModelTest(TestCase):
    def setUp(self):
        position = Position.objects.create(name="Test Position")
        self.worker = Worker.objects.create(
            username="test_user",
            first_name="John",
            last_name="Doe",
            position=position,
            phone_number="+123456789",
            country="US",
        )

    def test_create_worker(self):
        self.assertEqual(self.worker.username, "test_user")
        self.assertEqual(self.worker.first_name, "John")
        self.assertEqual(self.worker.last_name, "Doe")
        self.assertEqual(self.worker.position.name, "Test Position")
        self.assertEqual(self.worker.phone_number, "+123456789")
        self.assertEqual(str(self.worker),
                         "test_user (John Doe) - Test Position")


class TeamModelTest(TestCase):
    def setUp(self):
        project = Project.objects.create(name="Test Project")
        position = Position.objects.create(name="Test Position")
        worker = Worker.objects.create(
            username="test_user",
            first_name="John",
            last_name="Doe",
            position=position,
            phone_number="+123456789",
            country="US",
        )
        self.team = Team.objects.create(
            name="Test Team",
        )
        self.team.projects.add(project)
        self.team.workers.add(worker)

    def test_create_team(self):
        self.assertEqual(self.team.name, "Test Team")
        self.assertEqual(self.team.projects.first().name, "Test Project")
        self.assertEqual(self.team.workers.first().username, "test_user")

    def test_team_str_method(self):
        self.assertEqual(str(self.team), "Test Team")
