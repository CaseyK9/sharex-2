# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-16 19:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0016_auto_20180416_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 17, 19, 17, 35, 984256, tzinfo=utc), verbose_name='expire'),
        ),
    ]