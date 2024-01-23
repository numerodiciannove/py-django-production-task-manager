# Generated by Django 4.2.9 on 2024-01-16 21:11

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):
    dependencies = [
        ("task_manager", "0032_alter_project_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="worker",
            name="country",
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
    ]