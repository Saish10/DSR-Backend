# Generated by Django 5.0.1 on 2024-04-05 05:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worklog', '0002_project_assigned_user_project_tenant'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='assigned_user',
        ),
        migrations.AddField(
            model_name='project',
            name='assigned_users',
            field=models.ManyToManyField(blank=True, related_name='assigned_projects', to=settings.AUTH_USER_MODEL, verbose_name='assigned users'),
        ),
    ]