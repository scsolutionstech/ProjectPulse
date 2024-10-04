# Generated by Django 5.1.1 on 2024-09-27 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="billing_status",
            field=models.CharField(
                choices=[
                    ("billable", "Billable"),
                    ("non_billable", "Non-Billable"),
                    ("partial", "Partially Billable"),
                ],
                default="billable",
                max_length=20,
            ),
        ),
    ]
