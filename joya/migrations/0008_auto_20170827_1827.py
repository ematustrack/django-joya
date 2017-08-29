# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-27 18:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joya', '0007_auto_20170827_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='phone',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Telefono'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='website',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='WebSite'),
        ),
    ]
