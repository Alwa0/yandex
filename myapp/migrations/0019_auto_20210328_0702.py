# Generated by Django 2.2.12 on 2021-03-28 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_auto_20210328_0700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courier',
            name='orders',
        ),
        migrations.AddField(
            model_name='courier',
            name='orders',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='myapp.Order'),
        ),
    ]
