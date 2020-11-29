# Generated by Django 3.1.3 on 2020-11-27 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChemicalElement',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=80)),
                ('inventory', models.SmallIntegerField()),
                ('price', models.SmallIntegerField()),
                ('element_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metallics_api.chemicalelement')),
            ],
        ),
        migrations.CreateModel(
            name='ChemicalConcentration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.SmallIntegerField()),
                ('commodity_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metallics_api.commodity')),
                ('element_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metallics_api.chemicalelement')),
            ],
        ),
    ]