from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_complete = models.BooleanField(default=False, db_index=True)
    description = models.TextField(null=True, blank=True)
    budget = models.IntegerField(null=True, blank=True)

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
    description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tasks"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        null=True,
        blank=True,
    )
    task_type = models.ManyToManyField(
        TaskType,
        related_name="tasks"
    )

    class Meta:
        ordering = ["name", ]

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(
        max_length=100, unique=True,
    )

    class Meta:
        ordering = ["name", ]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        max_length=13,
        help_text="For example '+380951911919'. Without quotes"
    )
    country = CountryField(blank=True)

    class Meta:
        ordering = ["position", ]

    def __str__(self):
        return (
            f"{self.username} "
            f"({self.first_name} {self.last_name}) - {self.position}"
        )


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    projects = models.ManyToManyField(
        Project,
        blank=True,
        related_name="teams",
    )

    workers = models.ManyToManyField(
        Worker,
        blank=True,
        related_name="teams",
    )

    class Meta:
        ordering = ["name", ]

    def __str__(self):
        return self.name
