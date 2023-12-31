# Generated by Django 3.2.23 on 2024-01-02 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_products_public_schema_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_type',
            field=models.CharField(choices=[('stand_alone_product', 'Stand Alone Product'), ('parent_product', 'Parent Product')], default='stand_alone_product', max_length=30),
        ),
    ]
