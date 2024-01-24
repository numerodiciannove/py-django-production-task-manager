from unittest import TestCase

from task_manager.forms import ProjectTaskForm
from task_manager.models import Project, TaskType


class ProjectTaskFormTest(TestCase):
    @staticmethod
    def create_project(self, name="Test Project"):
        return Project.objects.create(name=name)

    @staticmethod
    def create_task_type(self, name="Test Type"):
        return TaskType.objects.create(name=name)

    def test_project_task_form_valid_data(self):
        project = self.create_project()
        task_type_1 = self.create_task_type(name="Type 1")
        task_type_2 = self.create_task_type(name="Type 2")

        form_data = {
            "is_complete": True,
            "name": "Test Task",
            "description": "This is a test task.",
            "start_time": "2022-01-01T12:00",
            "deadline": "2022-01-02T12:00",
            "priority": "low",
            "task_type": [task_type_1.id, task_type_2.id],
            "project": project.id,
        }

        form = ProjectTaskForm(data=form_data)

        if not form.is_valid():
            print("Form is not valid.")
            print("Errors:", form.errors)
            print("Cleaned Data:", form.cleaned_data)

        self.assertTrue(form.is_valid())
