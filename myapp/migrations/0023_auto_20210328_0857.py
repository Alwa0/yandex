# Generated by Django 2.2.12 on 2021-03-28 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_order_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courier',
            name='earnings',
            field=models.IntegerField(default=0),
        ),
    ]
