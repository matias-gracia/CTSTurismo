# Generated by Django 5.1.3 on 2024-11-29 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_winner',
            field=models.BooleanField(default=False),
        ),
    ]