# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-04 19:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0005_auto_20171213_0343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'truck'), (2, 'sedan'), (3, 'pickup'), (4, 'motorcycle')], default='1'),
        ),
    ]
