# Generated by Django 4.2.9 on 2024-01-11 21:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task_manager", "0025_alter_project_is_complete"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="workers",
            field=models.ManyToManyField(
                blank=True, related_name="workers", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
