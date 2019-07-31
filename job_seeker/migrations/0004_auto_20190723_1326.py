# Generated by Django 2.2.3 on 2019-07-23 07:41

from django.db import migrations, models
import home.validator


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0003_auto_20190723_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seekerdetail',
            name='phone_no',
            field=models.IntegerField(blank=True, validators=[home.validator.phone_no_validation]),
        ),
    ]
