# Generated by Django 3.2.23 on 2024-01-17 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0003_alter_plan_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='onboarding',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]