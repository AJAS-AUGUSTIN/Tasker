# Generated by Django 4.0.3 on 2022-03-11 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0002_applyjob_applied_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='applyjob',
            name='applied',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='applyjob',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
