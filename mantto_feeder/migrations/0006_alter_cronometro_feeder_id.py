# Generated by Django 5.1.2 on 2024-11-27 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantto_feeder', '0005_alter_cronometro_tiempo_inicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cronometro',
            name='feeder_id',
            field=models.CharField(max_length=255),
        ),
    ]
