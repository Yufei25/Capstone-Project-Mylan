# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-04 21:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lanapp', '0010_auto_20180504_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='location',
            field=models.CharField(default='Heading', max_length=100),
            preserve_default=False,
        ),
    ]