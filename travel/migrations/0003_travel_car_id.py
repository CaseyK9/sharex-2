# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-28 01:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_auto_20171213_0314'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='car_id',
            field=models.FloatField(blank=True, max_length=255, null=True),
        ),
    ]
