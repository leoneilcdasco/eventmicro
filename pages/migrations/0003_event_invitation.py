# Generated by Django 3.1.1 on 2020-10-13 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_event_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='invitation',
            field=models.TextField(blank=True),
        ),
    ]
