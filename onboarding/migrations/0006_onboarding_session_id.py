# Generated by Django 3.2.23 on 2023-12-13 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0005_onboarding_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='onboarding',
            name='session_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
