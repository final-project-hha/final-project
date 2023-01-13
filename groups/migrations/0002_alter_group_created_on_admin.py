# Generated by Django 4.1.3 on 2023-01-13 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='created_on',
            field=models.DateTimeField(default='2023-01-13 11:01'),
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('groups', models.ManyToManyField(related_name='admin',
                                                  to='groups.group')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.DO_NOTHING,
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),
    ]