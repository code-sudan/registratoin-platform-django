# Generated by Django 4.0 on 2022-03-03 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0014_remove_registration_batch'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeSudanQuote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quote', models.TextField()),
                ('by', models.TextField()),
            ],
        ),
    ]
