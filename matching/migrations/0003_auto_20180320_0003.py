# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-19 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0002_matching_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matching_list',
            name='travel_id',
            field=models.IntegerField(blank=True, max_length=255, null=True),
        ),
    ]
