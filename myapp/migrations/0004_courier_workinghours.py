# Generated by Django 2.2.12 on 2021-03-25 07:54

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_delete_courier'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkingHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.TimeField(default=datetime.time)),
                ('end', models.TimeField(default=datetime.time)),
            ],
        ),
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('F', 'foot'), ('C', 'car'), ('B', 'bike')], max_length=4)),
                ('regions', models.CharField(blank=True, max_length=50, validators=[django.core.validators.int_list_validator])),
                ('working_hours', models.ManyToManyField(to='myapp.WorkingHours')),
            ],
        ),
    ]
