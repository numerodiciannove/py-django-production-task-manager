# Generated by Django 5.0.1 on 2024-01-09 21:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task_manager", "0014_worker_team"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="worker",
            name="team",
        ),
        migrations.AddField(
            model_name="team",
            name="workers",
            field=models.ManyToManyField(
                blank=True, related_name="teams", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
