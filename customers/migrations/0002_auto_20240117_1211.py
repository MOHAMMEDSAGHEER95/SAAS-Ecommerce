# Generated by Django 3.2.23 on 2024-01-17 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='on_trial',
        ),
        migrations.RemoveField(
            model_name='client',
            name='on_trials',
        ),
    ]