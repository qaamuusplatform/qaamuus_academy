# Generated by Django 4.1 on 2023-01-08 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_couponcode_expiredate'),
        ('a_webinar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventenrolled',
            name='theUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolledEvents', to='api.userprofile'),
        ),
    ]
