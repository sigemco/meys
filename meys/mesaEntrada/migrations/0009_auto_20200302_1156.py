# Generated by Django 2.2.4 on 2020-03-02 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mesaEntrada', '0008_auto_20200302_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='origen',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mesaEntrada.unidades', verbose_name='Unidad de Origen:'),
        ),
    ]
