# Generated by Django 4.1 on 2022-09-13 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_userprofile_facebook_link_userprofile_third_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessons',
            name='lessonLink',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
    ]
