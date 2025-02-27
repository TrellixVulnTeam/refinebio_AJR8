# Generated by Django 2.2.10 on 2020-03-16 17:25

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_refinery_common", "0053_auto_20200122_2004"),
    ]

    operations = [
        migrations.CreateModel(
            name="DatasetAnnotation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("data", django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ("is_public", models.BooleanField(default=True)),
                (
                    "created_at",
                    models.DateTimeField(default=django.utils.timezone.now, editable=False),
                ),
                ("last_modified", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="data_refinery_common.Dataset",
                    ),
                ),
            ],
            options={
                "db_table": "dataset_annotations",
                "base_manager_name": "public_objects",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("public_objects", django.db.models.manager.Manager()),
            ],
        ),
    ]
