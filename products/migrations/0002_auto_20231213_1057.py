# Generated by Django 3.2.23 on 2023-12-13 10:57

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(null=True, upload_to=products.models.get_upload_path),
        ),
    ]
