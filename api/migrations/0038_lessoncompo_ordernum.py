# Generated by Django 4.1 on 2022-12-07 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_lessoncompo_lessonscount_lessoncompo_simdesc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessoncompo',
            name='orderNum',
            field=models.IntegerField(default=0),
        ),
    ]