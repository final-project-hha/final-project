# Generated by Django 4.1.3 on 2023-01-13 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_alter_group_created_on_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='created_on',
            field=models.DateTimeField(default='2023-01-13 13:01'),
        ),
    ]
