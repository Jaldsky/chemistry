# Generated by Django 4.2.19 on 2025-03-07 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_classinvitation_initiated_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activity_score',
            field=models.IntegerField(default=0, verbose_name='очки активности'),
        ),
    ]
