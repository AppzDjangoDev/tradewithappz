# Generated by Django 3.2.19 on 2024-06-08 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fyersapi', '0026_openordertempdata_sl_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='openordertempdata',
            name='exp_loss',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]
