# Generated by Django 4.2.7 on 2023-12-18 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_commodity_height_commodity_width_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commodity',
            name='height',
        ),
        migrations.RemoveField(
            model_name='commodity',
            name='width',
        ),
    ]
