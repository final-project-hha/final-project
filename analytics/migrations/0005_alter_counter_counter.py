# Generated by Django 4.1.2 on 2022-11-21 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_alter_counter_counter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='counter',
            field=models.IntegerField(default=0),
        ),
    ]
