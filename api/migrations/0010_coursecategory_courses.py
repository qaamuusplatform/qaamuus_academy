# Generated by Django 4.1 on 2022-08-22 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecategory',
            name='courses',
            field=models.IntegerField(default=1),
        ),
    ]
