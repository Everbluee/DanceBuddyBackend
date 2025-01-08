# Generated by Django 5.1.4 on 2025-01-08 17:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('BasicBackend', '0016_alter_danceclass_days'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='danceclassattendance',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='danceclassattendance',
            name='session_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='danceclassattendance',
            unique_together={('user', 'dance_class', 'session_date')},
        ),
    ]
