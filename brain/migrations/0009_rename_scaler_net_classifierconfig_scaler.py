# Generated by Django 4.2.3 on 2023-08-01 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0008_classifierconfig_neural_net_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classifierconfig',
            old_name='scaler_net',
            new_name='scaler',
        ),
    ]
