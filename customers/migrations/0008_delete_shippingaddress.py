# Generated by Django 3.2.23 on 2024-01-07 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20240107_1826'),
        ('customers', '0007_alter_shippingaddress_unique_together'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShippingAddress',
        ),
    ]
