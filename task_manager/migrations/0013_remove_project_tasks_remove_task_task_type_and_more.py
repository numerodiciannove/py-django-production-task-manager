# Generated by Django 5.0.1 on 2024-01-09 20:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task_manager", "0012_project_is_complete"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="tasks",
        ),
        migrations.RemoveField(
            model_name="task",
            name="task_type",
        ),
        migrations.AddField(
            model_name="task",
            name="project",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="task_manager.project",
            ),
        ),
        migrations.AddField(
            model_name="tasktype",
            name="task",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="task_manager.task",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="deadline",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.CharField(
                blank=True,
                choices=[
                    ("urgent", "Urgent"),
                    ("height", "Height"),
                    ("medium", "Medium"),
                    ("low", "Low"),
                ],
                max_length=10,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="start_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
