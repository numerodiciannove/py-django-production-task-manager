# Generated by Django 5.0.1 on 2024-01-10 00:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("task_manager", "0020_remove_team_worker_team_worker"),
    ]

    operations = [
        migrations.RenameField(
            model_name="team",
            old_name="worker",
            new_name="workers",
        ),
    ]