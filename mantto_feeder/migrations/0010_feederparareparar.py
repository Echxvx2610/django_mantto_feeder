# Generated by Django 5.1.2 on 2025-04-07 23:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantto_feeder', '0009_partesfeeder_estado_partesfeeder_stock_minimo'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeederParaReparar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feeder_id', models.IntegerField()),
                ('tamano', models.CharField(max_length=5)),
                ('color', models.CharField(max_length=20)),
                ('falla', models.CharField(max_length=255)),
                ('cantidad_refaccion', models.IntegerField()),
                ('tecnico', models.CharField(max_length=50)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('parte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mantto_feeder.partesfeeder')),
            ],
        ),
    ]
