# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-10 04:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0008_auto_20180410_0435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 11, 4, 38, 19, 267909, tzinfo=utc), verbose_name='expire'),
        ),
    ]
