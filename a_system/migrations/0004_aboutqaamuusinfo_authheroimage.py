# Generated by Django 4.1 on 2022-09-01 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_system', '0003_aboutqaamuusinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutqaamuusinfo',
            name='authHeroImage',
            field=models.ImageField(blank=True, null=True, upload_to='images/aboutQaamuus'),
        ),
    ]
