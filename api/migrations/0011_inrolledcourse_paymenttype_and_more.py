# Generated by Django 4.1 on 2022-12-31 08:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_inrolledcourse_paymenttype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inrolledcourse',
            name='paymentType',
            field=models.CharField(default='waafi', max_length=255),
        ),
        migrations.AlterField(
            model_name='couponcode',
            name='expireDate',
            field=models.DateField(default=datetime.datetime(2023, 1, 2, 11, 4, 38, 350235)),
        ),
        migrations.AlterField(
            model_name='qacourses',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructorCourses', to='api.userprofile'),
        ),
    ]