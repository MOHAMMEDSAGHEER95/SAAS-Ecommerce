# Generated by Django 3.2.23 on 2023-12-10 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20231210_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='on_trials',
            field=models.BooleanField(default=True),
        ),
    ]
