# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-21 21:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lanapp', '0009_contentcomment_warningcomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paragraphs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True)),
                ('index', models.IntegerField()),
                ('highlight', models.BooleanField()),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lanapp.Contract')),
            ],
        ),
    ]
