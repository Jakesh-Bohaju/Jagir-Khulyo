# Generated by Django 2.2.3 on 2019-07-31 02:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0007_auto_20190731_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seekerdetail',
            name='education',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seeker_detail_education', to='home.Education'),
        ),
        migrations.AlterField(
            model_name='seekerdetail',
            name='gender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seeker_detail_gender', to='home.Gender'),
        ),
        migrations.AlterField(
            model_name='seekerdetail',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seeker_detail_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
