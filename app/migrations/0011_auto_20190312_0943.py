# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-03-12 09:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_order'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='order',
            table='axf_order',
        ),
    ]