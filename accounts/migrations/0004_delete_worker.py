# Generated by Django 4.0.3 on 2022-03-15 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_worker'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Worker',
        ),
    ]
