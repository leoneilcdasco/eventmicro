# Generated by Django 3.1.1 on 2020-11-08 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_auto_20201108_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='appointment',
            field=models.TextField(blank=True),
        ),
    ]
