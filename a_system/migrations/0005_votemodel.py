# Generated by Django 4.1 on 2022-10-04 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_system', '0004_aboutqaamuusinfo_authheroimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('magaca', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('phoneNumber', models.CharField(max_length=255)),
                ('qaabkaWaxbarashada', models.CharField(max_length=255)),
                ('maadadaAadDaneeneeso', models.CharField(max_length=255)),
                ('waqtiga', models.CharField(max_length=255)),
                ('macalimiinta', models.CharField(max_length=255)),
            ],
        ),
    ]
