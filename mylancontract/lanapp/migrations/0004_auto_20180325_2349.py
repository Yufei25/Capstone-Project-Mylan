# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-25 23:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lanapp', '0003_auto_20180325_2343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchresult',
            name='contents',
        ),
        migrations.AddField(
            model_name='searchresult',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.DeleteModel(
            name='Content',
        ),
    ]
