# Generated by Django 3.2.23 on 2024-01-19 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_products_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='search_keywords',
            field=models.TextField(blank=True, null=True),
        ),
    ]