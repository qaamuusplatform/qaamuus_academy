# Generated by Django 4.1 on 2023-01-11 10:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_userprofile_refbalance_userprofile_refwithdraw_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='referraltransaction',
            old_name='theUser',
            new_name='theReffUser',
        ),
        migrations.AddField(
            model_name='referraltransaction',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='couponcode',
            name='expireDate',
            field=models.DateField(default=datetime.datetime(2023, 1, 13, 13, 39, 37, 55292)),
        ),
    ]