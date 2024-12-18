# Generated by Django 5.1.2 on 2024-12-04 16:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('BasicBackend', '0013_danceclassassignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='danceclass',
            name='users',
            field=models.ManyToManyField(related_name='dance_classes', through='BasicBackend.DanceClassAssignment',
                                         to=settings.AUTH_USER_MODEL),
        ),
    ]
