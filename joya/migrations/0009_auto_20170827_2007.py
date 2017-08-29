# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-27 20:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joya', '0008_auto_20170827_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemsClient',
            fields=[
            ],
            options={
                'verbose_name': 'Inventario Clientes',
                'proxy': True,
                'indexes': [],
            },
            bases=('joya.items',),
        ),
        migrations.AddField(
            model_name='items',
            name='size',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Talla'),
        ),
        migrations.AddField(
            model_name='items',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Activo'),
        ),
    ]
