# Generated by Django 5.1.1 on 2024-09-22 15:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0006_alter_invitation_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="position",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT, to="employees.position"
            ),
        ),
    ]
