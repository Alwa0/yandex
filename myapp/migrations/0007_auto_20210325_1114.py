# Generated by Django 2.2.12 on 2021-03-25 11:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20210325_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courier',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='weight',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(50), django.core.validators.MinValueValidator(0.01)]),
        ),
    ]
