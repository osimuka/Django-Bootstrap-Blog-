# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0006_auto_20171110_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(default=None, upload_to='Blog/static/img/blog_img/'),
        ),
    ]