# Generated by Django 4.0.3 on 2022-03-09 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.AddField(
            model_name='user',
            name='is_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_worker',
            field=models.BooleanField(default=False),
        ),
    ]
