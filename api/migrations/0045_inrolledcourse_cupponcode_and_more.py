# Generated by Django 4.1 on 2022-12-14 07:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_userprofile_city_alter_couponcode_expiredate'),
    ]

    operations = [
        migrations.AddField(
            model_name='inrolledcourse',
            name='cupponCode',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='inrolledcourse',
            name='referralCode',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='couponcode',
            name='expireDate',
            field=models.DateField(default=datetime.datetime(2022, 12, 16, 10, 18, 40, 226692)),
        ),
    ]