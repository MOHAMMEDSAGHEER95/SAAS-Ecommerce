# Generated by Django 3.2.23 on 2023-12-25 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('placed', 'Placed'), ('packed', 'Packed'), ('shipped', 'Shippped'), ('delivered', 'Delivered')], default='placed', max_length=30),
        ),
    ]