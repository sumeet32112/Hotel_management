# Generated by Django 3.2.8 on 2021-11-28 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0010_auto_20211125_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='room_type',
        ),
    ]
