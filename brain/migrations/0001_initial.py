# Generated by Django 4.2.3 on 2023-07-28 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VisitorBehavior',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_spent', models.IntegerField()),
                ('pages_visited', models.IntegerField()),
                ('conversion_target_a', models.IntegerField(default=0)),
                ('conversion_target_b', models.IntegerField(default=0)),
            ],
        ),
    ]
