# Generated by Django 4.1 on 2022-12-26 08:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0056_alter_couponcode_expiredate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponcode',
            name='expireDate',
            field=models.DateField(default=datetime.datetime(2022, 12, 28, 11, 3, 1, 782261)),
        ),
    ]