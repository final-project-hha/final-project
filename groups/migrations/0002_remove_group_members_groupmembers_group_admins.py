# Generated by Django 4.1.2 on 2022-11-17 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='members',
        ),
        migrations.CreateModel(
            name='GroupMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('AD', 'Admin'), ('MR', 'Member')], default='MR', max_length=2)),
                ('joined_on', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.group')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_member', to='users.member')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='admins',
            field=models.ManyToManyField(through='groups.GroupMembers', to='users.member'),
        ),
    ]
