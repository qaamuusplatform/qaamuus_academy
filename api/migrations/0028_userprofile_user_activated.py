# Generated by Django 4.1 on 2022-09-22 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_alter_lessons_lessonlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_activated',
            field=models.BooleanField(default=False),
        ),
    ]
