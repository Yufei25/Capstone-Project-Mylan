# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class SearchResult(models.Model):
    filename = models.CharField(max_length=400)
    keyword = models.CharField(max_length=100)
    content = models.TextField(blank=True)

    def __unicode__(self):
        return self.filename + '\t' + self.keyword + '\t' + self.content


class Contract(models.Model):
    filename = models.CharField(max_length=400)
    contract = models.FileField(upload_to='contracts')

    def __unicode__(self):
        return self.filename
