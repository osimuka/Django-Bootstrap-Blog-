# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-10 14:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0002_auto_20171110_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomments',
            name='date',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
