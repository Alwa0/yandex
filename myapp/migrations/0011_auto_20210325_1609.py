# Generated by Django 2.2.12 on 2021-03-25 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_auto_20210325_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='assign_time',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
