# Generated by Django 5.0.2 on 2024-03-01 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth_api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("client", "Client"),
                    ("admin", "Admin"),
                    ("garage_owner", "Garage Owner"),
                ],
                default="client",
                max_length=50,
            ),
        ),
    ]