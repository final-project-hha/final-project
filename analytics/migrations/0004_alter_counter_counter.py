# Generated by Django 4.1.2 on 2022-11-21 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_alter_counter_counter_alter_counter_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='counter',
            field=models.IntegerField(null=True),
        ),
    ]
