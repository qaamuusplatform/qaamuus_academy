# Generated by Django 4.1 on 2022-09-23 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_webinar', '0006_alter_eventview_videourl'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventview',
            old_name='isLandscape',
            new_name='isLiveIcon',
        ),
        migrations.RenameField(
            model_name='eventview',
            old_name='isLive',
            new_name='isRealLiveSdk',
        ),
        migrations.AddField(
            model_name='eventview',
            name='join_URL',
            field=models.CharField(blank=True, max_length=555),
        ),
        migrations.AddField(
            model_name='eventview',
            name='meetingNumber',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='eventview',
            name='meetingPassword',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
