# Generated by Django 2.2.3 on 2019-07-31 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_district_province_no'),
        ('company', '0007_auto_20190731_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='companydetail',
            name='district',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='company_detail_district', to='home.District'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companydetail',
            name='province',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='company_detail_province', to='home.Province'),
            preserve_default=False,
        ),
    ]
