# Generated by Django 3.1.3 on 2020-11-29 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metallics_api', '0005_auto_20201129_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodity',
            name='inventory',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]