# Generated by Django 3.1.3 on 2020-11-28 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metallics_api', '0002_auto_20201127_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commodity',
            name='element_id',
        ),
        migrations.AddField(
            model_name='commodity',
            name='chemical_composition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='chemical_compositions', to='metallics_api.commodity'),
        ),
        migrations.RemoveField(
            model_name='chemicalconcentration',
            name='element_id',
        ),
        migrations.AddField(
            model_name='chemicalconcentration',
            name='element_id',
            field=models.ManyToManyField(to='metallics_api.ChemicalElement'),
        ),
        migrations.AlterModelTable(
            name='chemicalconcentration',
            table='ChemicalConcentration',
        ),
        migrations.AlterModelTable(
            name='chemicalelement',
            table='ChemicalElement',
        ),
        migrations.AlterModelTable(
            name='commodity',
            table='Commodity',
        ),
    ]