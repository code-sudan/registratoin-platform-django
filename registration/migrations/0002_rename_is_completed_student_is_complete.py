# Generated by Django 3.2.5 on 2021-12-29 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='is_completed',
            new_name='is_complete',
        ),
    ]
