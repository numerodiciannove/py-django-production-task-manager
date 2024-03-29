# Generated by Django 5.0.1 on 2024-01-09 20:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task_manager", "0013_remove_project_tasks_remove_task_task_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="worker",
            name="team",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="task_manager.team",
            ),
        ),
    ]
