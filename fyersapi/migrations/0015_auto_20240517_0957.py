# Generated by Django 3.2.19 on 2024-05-17 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fyersapi', '0014_auto_20240515_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='sod_eod_data',
            name='eod_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sod_eod_data',
            name='sod_status',
            field=models.BooleanField(default=False),
        ),
    ]
