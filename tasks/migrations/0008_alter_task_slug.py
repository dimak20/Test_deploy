# Generated by Django 5.1.1 on 2024-09-24 11:31

import django_extensions.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0007_alter_task_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="slug",
            field=django_extensions.db.fields.AutoSlugField(
                blank=True,
                editable=False,
                max_length=100,
                populate_from=["name"],
                unique=True,
            ),
        ),
    ]
