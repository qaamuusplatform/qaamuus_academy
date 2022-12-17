# Generated by Django 4.1 on 2022-12-17 06:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_alter_couponcode_expiredate'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotifications',
            name='title',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='couponcode',
            name='expireDate',
            field=models.DateField(default=datetime.datetime(2022, 12, 19, 9, 55, 13, 847167)),
        ),
    ]
