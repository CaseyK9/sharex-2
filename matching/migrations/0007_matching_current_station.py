# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-08 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0006_auto_20180407_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='matching',
            name='current_station',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
