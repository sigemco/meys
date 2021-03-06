# Generated by Django 2.2.4 on 2020-03-02 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mesaEntrada', '0005_auto_20200229_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='destino',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='destino', to='mesaEntrada.unidades', verbose_name='Unidad de Destino:'),
        ),
        migrations.AlterField(
            model_name='documento',
            name='origen',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='origen', to='mesaEntrada.unidades', verbose_name='Unidad de Origen:'),
        ),
    ]
