# Generated by Django 4.1.2 on 2022-10-31 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='charges',
            options={'verbose_name_plural': 'Charges'},
        ),
    ]