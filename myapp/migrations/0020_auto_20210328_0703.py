# Generated by Django 2.2.12 on 2021-03-28 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_auto_20210328_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courier',
            name='orders',
            field=models.ManyToManyField(blank=True, default=None, to='myapp.Order'),
        ),
    ]
