# Generated by Django 4.0.3 on 2022-03-16 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0006_alter_reviewrating_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.job'),
        ),
        migrations.AlterField(
            model_name='reviewrating',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reviewrating',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='worker_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
