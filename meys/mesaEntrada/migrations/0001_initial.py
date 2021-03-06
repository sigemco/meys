# Generated by Django 3.0.3 on 2020-02-26 16:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='tipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Tipo',
                'verbose_name_plural': 'Tipos',
            },
        ),
        migrations.CreateModel(
            name='unidades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidad', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='documento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nro_sistema', models.CharField(max_length=50)),
                ('Fecha_entrada', models.DateField(default=django.utils.timezone.now)),
                ('Fecha_salida', models.DateField(auto_now=True)),
                ('Fecha_registro', models.DateField(auto_now=True)),
                ('asunto', models.CharField(max_length=200)),
                ('Termino', models.DateField()),
                ('Termino_interno', models.DateField()),
                ('Obs', models.CharField(max_length=200)),
                ('archivo', models.FileField(upload_to='')),
                ('Estado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mesaEntrada.estado')),
                ('Tipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mesaEntrada.tipo')),
                ('origen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mesaEntrada.unidades')),
            ],
        ),
    ]
