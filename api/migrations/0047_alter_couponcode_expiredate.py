# Generated by Django 4.1 on 2022-12-14 07:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_alter_couponcode_expiredate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponcode',
            name='expireDate',
            field=models.DateField(default=datetime.datetime(2022, 12, 16, 10, 19, 7, 607439)),
        ),
    ]
