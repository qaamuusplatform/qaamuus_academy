# Generated by Django 4.1 on 2023-01-08 15:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_couponcode_expiredate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponcode',
            name='expireDate',
            field=models.DateField(default=datetime.datetime(2023, 1, 10, 18, 35, 8, 316427)),
        ),
    ]
