# Generated by Django 4.1.3 on 2023-01-25 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0008_alter_group_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='created_on',
            field=models.DateTimeField(default='2023-01-25 11:01'),
        ),
    ]
