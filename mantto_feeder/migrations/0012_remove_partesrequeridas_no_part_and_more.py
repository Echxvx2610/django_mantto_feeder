# Generated by Django 5.1.2 on 2025-04-08 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantto_feeder', '0011_partesrequeridas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partesrequeridas',
            name='no_part',
        ),
        migrations.AddField(
            model_name='partesrequeridas',
            name='numero_parte',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mantto_feeder.partesfeeder'),
        ),
    ]
