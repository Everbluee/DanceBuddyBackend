# Generated by Django 5.1.4 on 2025-01-10 14:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('BasicBackend', '0017_alter_danceclassattendance_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='danceclassattendance',
            name='session_date',
            field=models.DateField(),
        ),
    ]
