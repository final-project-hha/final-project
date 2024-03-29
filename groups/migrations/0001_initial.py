# Generated by Django 4.1.3 on 2023-01-13 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('created_by', models.CharField(max_length=255)),
                ('group_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_on', models.DateTimeField(
                    default='2023-01-13 09:01'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.DO_NOTHING,
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),
    ]
