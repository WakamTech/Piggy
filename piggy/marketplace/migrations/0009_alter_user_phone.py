# Generated by Django 5.0.6 on 2024-07-17 03:19

import marketplace.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0008_pricerule_ad_initial_price_per_kg_order_livraison'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=15, unique=True, validators=[marketplace.validators.validate_phone]),
        ),
    ]
