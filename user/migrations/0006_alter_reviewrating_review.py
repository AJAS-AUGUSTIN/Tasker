# Generated by Django 4.0.3 on 2022-03-16 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_reviewrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='review',
            field=models.CharField(max_length=500),
        ),
    ]
