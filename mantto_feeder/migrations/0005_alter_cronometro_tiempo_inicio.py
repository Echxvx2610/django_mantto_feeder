# Generated by Django 5.1.2 on 2024-11-26 00:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantto_feeder', '0004_cronometro_feeder_id_alter_cronometro_tiempo_inicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cronometro',
            name='tiempo_inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]