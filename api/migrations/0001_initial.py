# Generated by Django 3.2.3 on 2021-05-19 06:22

import api.models
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
            name='Profile',
            fields=[
                ('id', models.CharField(default=api.models.generate_unique_id, editable=False, max_length=16, primary_key=True, serialize=False, unique=True)),
                ('institute', models.CharField(choices=[('IIITRANCHI', 'Indian Institute of Information Technology Ranchi'), ('INSTI_A', 'Institute A'), ('INSTI_B', 'Institute B'), ('INSTI_C', 'Institute C'), ('INSTI_D', 'Institute D'), ('OTHER', 'Other Institute')], default='IIITRANCHI', max_length=100, verbose_name='institute name')),
                ('branch', models.CharField(choices=[('CSE_UG', 'Computer Science and Engineering (Undergraduate)'), ('ECE_UG', 'Electronics and Communications Engineering (Undergraduate)')], default='CSE_UG', max_length=100, verbose_name='branch')),
                ('year', models.CharField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior')], default='FR', max_length=2, verbose_name='year')),
                ('github_url', models.URLField(blank=True, max_length=255, null=True, verbose_name='github url')),
                ('primary_language', models.CharField(choices=[('PY', 'Python'), ('CPP', 'C++'), ('C', 'C'), ('JAVA', 'Java')], default='PY', max_length=5, verbose_name='primary programming language')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
