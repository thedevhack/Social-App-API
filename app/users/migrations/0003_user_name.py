# Generated by Django 5.0.6 on 2024-06-03 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_groups_user_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]