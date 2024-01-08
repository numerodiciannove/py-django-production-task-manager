from django.db import models
from django.contrib.auth.models import AbstractUser


class Position(models.Model):
    name = models.CharField(
        max_length=100, unique=True,
    )

    class Meta:
        ordering = ["name", ]

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(
        max_length=100,
    )

    class Meta:
        ordering = ["name", ]

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("urgent", "Urgent"),
        ("height", "Height"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    name = models.CharField(max_length=255, )
    description = models.TextField()
    start_time = models.DateTimeField(null=True)
    deadline = models.DateTimeField(null=True)
    is_complete = models.BooleanField(default=False)
    task_type = models.ManyToManyField(
        TaskType,
        blank=True,
        related_name="tasks",
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
    )

    class Meta:
        ordering = ["name", ]

    def __str__(self):
        return self.name


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

    class Meta:
        ordering = ["position", ]

    def __str__(self):
        return (
            f"{self.username} "
            f"({self.first_name} {self.last_name}) - {self.position}"
        )


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_complete = models.BooleanField(default=False)
    tasks = models.ManyToManyField(
        Task,
        related_name="projects",
    )

    class Meta:
        ordering = ["name", ]

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    projects = models.ManyToManyField(
        Project,
        blank=True,
        related_name="teams",
    )

    class Meta:
        ordering = ["name", ]

    def __str__(self):
        return self.name
