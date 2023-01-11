# Generated by Django 4.1 on 2023-01-08 15:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_inrolledcourse_paided_alter_couponcode_expiredate'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='summerInfo',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='couponcode',
            name='expireDate',
            field=models.DateField(default=datetime.datetime(2023, 1, 10, 18, 33, 25, 676082)),
        ),
        migrations.AlterField(
            model_name='inrolledcourse',
            name='theUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolledCourses', to='api.userprofile'),
        ),
    ]