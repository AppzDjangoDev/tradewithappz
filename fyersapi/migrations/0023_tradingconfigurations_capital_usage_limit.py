# Generated by Django 3.2.19 on 2024-06-07 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fyersapi', '0022_rename_capital_usage_limit_tradingconfigurations_capital_limit_per_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradingconfigurations',
            name='capital_usage_limit',
            field=models.IntegerField(default=0),
        ),
    ]
