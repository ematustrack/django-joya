# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-18 01:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joya', '0005_auto_20170517_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='owner',
            field=models.CharField(choices=[('0', 'Fe\xf1a'), ('1', 'Fe\xf1a-Eduardo')], default='Fe\xf1a-Eduardo', max_length=20),
        ),
        migrations.AddField(
            model_name='items',
            name='provider_code',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Codigo proveedor'),
        ),
        migrations.AddField(
            model_name='items',
            name='sell_price',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Venta'),
        ),
        migrations.AlterField(
            model_name='items',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Descripcion'),
        ),
    ]