# Generated by Django 3.2.23 on 2024-01-10 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='status',
            field=models.CharField(choices=[('Open', 'Open - currently active'), ('Submitted', 'Submitted - has been ordered at the checkout'), ('Merged', 'Merged - has been merged with old basket')], default='Open', max_length=100),
        ),
    ]
