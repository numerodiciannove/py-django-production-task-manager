from django.db import models
from django.contrib.auth.models import AbstractUser


class Position(models.Model):
    name = models.CharField(
        max_length=100, unique=True,
    )


class TaskType(models.Model):
    name = models.CharField(
        max_length=100,
    )


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("urgent", "Urgent"),
        ("height", "Height"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]
    name = models.CharField(max_length=255, )
    description = models.TextField()
    deadline = models.DateField()
    is_complete = models.BooleanField(default=False)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
    )

    class Meta:
        ordering = ["name"]


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        null=True
    )
    phone_number = models.CharField(
        max_length=13,
        unique=True,
        help_text="For example '+380951911919'. Without quotes"
    )

    def __str__(self):
        return (
            f"{self.username}: "
            f"({self.first_name} {self.last_name}) {self.position}"
        )


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    tasks = models.ManyToManyField(
        Task,
        related_name="projects",
    )

    class Meta:
        ordering = ["name", ]

    def __str__(self):
        return f"{self.name}: ({self.tasks})"


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    projects = models.ManyToManyField(
        Project,
        related_name="teams",
    )

    class Meta:
        ordering = ["name", ]
