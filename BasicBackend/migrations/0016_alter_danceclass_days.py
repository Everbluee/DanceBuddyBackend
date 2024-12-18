# Generated by Django 5.1.2 on 2024-12-04 17:10

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('BasicBackend', '0015_rename_classattendance_danceclassattendance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='danceclass',
            name='days',
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'),
                         ('thursday', 'Thursday'), ('friday', 'Friday')], max_length=40),
        ),
    ]
