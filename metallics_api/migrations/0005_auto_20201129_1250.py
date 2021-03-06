# Generated by Django 3.1.3 on 2020-11-29 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metallics_api', '0004_auto_20201128_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chemical',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, unique=True)),
            ],
            options={
                'db_table': 'chemical',
            },
        ),
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'composition',
            },
        ),
        migrations.RemoveField(
            model_name='commodity',
            name='chemical_composition',
        ),
        migrations.AlterField(
            model_name='commodity',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='commodity',
            name='inventory',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='commodity',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='commodity',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterModelTable(
            name='commodity',
            table='commodity',
        ),
        migrations.DeleteModel(
            name='ChemicalConcentration',
        ),
        migrations.DeleteModel(
            name='ChemicalElement',
        ),
        migrations.AddField(
            model_name='composition',
            name='commodity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metallics_api.commodity'),
        ),
        migrations.AddField(
            model_name='composition',
            name='element',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metallics_api.chemical'),
        ),
    ]
