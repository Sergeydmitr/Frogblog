# Generated by Django 3.0.6 on 2020-05-17 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200515_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='frog_lover',
            field=models.BooleanField(default=False),
        ),
    ]
