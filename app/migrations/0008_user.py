# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-03-10 06:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_goods'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=256)),
                ('phone', models.IntegerField()),
                ('img', models.CharField(max_length=40)),
                ('rank', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'axf_user',
            },
        ),
    ]
