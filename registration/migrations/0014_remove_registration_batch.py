# Generated by Django 4.0 on 2022-01-12 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0013_alter_registration_batch_alter_registration_program'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='batch',
        ),
    ]
