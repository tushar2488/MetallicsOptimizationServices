# Generated by Django 3.1.3 on 2020-11-27 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metallics_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodity',
            name='inventory',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='commodity',
            name='price',
            field=models.FloatField(),
        ),
    ]