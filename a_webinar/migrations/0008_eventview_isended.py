# Generated by Django 4.1 on 2022-09-27 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_webinar', '0007_rename_islandscape_eventview_isliveicon_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventview',
            name='isEnded',
            field=models.BooleanField(default=False),
        ),
    ]
