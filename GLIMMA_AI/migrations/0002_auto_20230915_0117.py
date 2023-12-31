# Generated by Django 3.2.21 on 2023-09-15 01:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('GLIMMA_AI', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userresponse',
            name='created_at',
        ),
        migrations.AddField(
            model_name='userresponse',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='answer',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='question',
            field=models.TextField(),
        ),
    ]
