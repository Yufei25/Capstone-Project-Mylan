# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.db.models import Max
import os


class SearchResult(models.Model):
    filename = models.CharField(max_length=400)
    keyword = models.CharField(max_length=100)
    content = models.TextField(blank=True)

    def __unicode__(self):
        return self.filename + '\t' + self.keyword + '\t' + self.content


class Contract(models.Model):
    filename = models.CharField(max_length=400)
    contract = models.FileField(upload_to='contracts')
    title = models.CharField(max_length=400, default='No Title')
    upload_time = models.DateTimeField(auto_now_add=True,null=True)
    last_changed = models.DateTimeField(auto_now=True)

    def delete(self,*args,**kwargs):
        if os.path.isfile(self.contract.path):
            os.remove(self.contract.path)
        super(Contract, self).delete(*args,**kwargs)

    def __unicode__(self):
        return self.filename

    # Returns all recent additions and deletions to the to-do list.
    @staticmethod
    def get_changes(changetime="1970-01-01T00:00+00:00"):
        return Contract.objects.filter(last_changed__gt=changetime).distinct()

    # https://docs.djangoproject.com/en/1.11/topics/templates/
    @property
    def html(self):
        return render_to_string("format/contract.html",
                                {"contract_id": self.id, "filename": self.filename, "contract": self.contract,
                                 "title": self.title, "upload_time": self.upload_time}).replace("\n", "")

    @staticmethod
    def get_max_time():
        return Contract.objects.all().aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"

class Paragraphs(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    index = models.IntegerField()
    highlight = models.BooleanField(default=False)
    endflag = models.BooleanField(default=False)
    warningflag = models.BooleanField(default=False)
    blankflag = models.BooleanField(default=False)

    def __unicode__(self):
        return self.filename

class ContractComment(models.Model):
    comment = models.TextField(blank=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    last_changed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.comment

    @staticmethod
    def get_changes(id, changeTime="1970-01-01T00:00+00:00"):
        contract = Contract.objects.get(id=id)
        comments = ContractComment.objects.filter(contract=contract, last_changed__gt=changeTime).distinct().order_by(
            "time")
        return comments

    @property
    def html(self):
        return render_to_string("format/contract_comment.html", {"comment_id": self.id, "comment": self.comment,
                                                                   "time": self.time}).replace("\n", "")

    @staticmethod
    def get_max_time():
        return ContractComment.objects.all().aggregate(Max('last_changed'))['last_changed__max'] \
               or "1970-01-01T00:00+00:00"


class Content(models.Model):
    content = models.TextField(blank=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100, default='test_keyword')
    time = models.DateTimeField(auto_now_add=True)
    last_changed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content

    @staticmethod
    def get_changes(id, changeTime="1970-01-01T00:00+00:00"):
        contract = Contract.objects.get(id=id)
        contents = Content.objects.filter(contract=contract, last_changed__gt=changeTime).distinct().order_by("time")
        return contents

    @property
    def html(self):
        return render_to_string("format/content.html", {"content_id": self.id, "content": self.content,
                                                          "time": self.time, "keyword": self.keyword}).replace("\n", "")

    @staticmethod
    def get_max_time():
        return Content.objects.all().aggregate(Max('last_changed'))['last_changed__max'] \
               or "1970-01-01T00:00+00:00"


class ContentComment(models.Model):
    comment = models.TextField(blank=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    last_changed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.comment

    @staticmethod
    def get_changes(id, changeTime="1970-01-01T00:00+00:00"):
        content = Content.objects.get(id=id)
        comments = ContentComment.objects.filter(content=content, last_changed__gt=changeTime).distinct().order_by(
            "time")
        return comments

    @property
    def html(self):
        return render_to_string("format/content_comment.html", {"comment_id": self.id, "comment": self.comment,
                                                                   "time": self.time}).replace("\n", "")

    @staticmethod
    def get_max_time():
        return ContentComment.objects.all().aggregate(Max('last_changed'))['last_changed__max'] \
               or "1970-01-01T00:00+00:00"


class Warning(models.Model):
    warning = models.TextField(blank=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100, default='test_warning')
    time = models.DateTimeField(auto_now_add=True)
    last_changed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.warning

    @staticmethod
    def get_changes(id, changeTime="1970-01-01T00:00+00:00"):
        contract = Contract.objects.get(id=id)
        warnings = Warning.objects.filter(contract=contract, last_changed__gt=changeTime).distinct().order_by("time")
        return warnings

    @property
    def html(self):
        return render_to_string("format/warning.html", {"warning_id": self.id, "warning": self.warning,
                                                          "time": self.time, "keyword": self.keyword}).replace("\n", "")

    @staticmethod
    def get_max_time():
        return Content.objects.all().aggregate(Max('last_changed'))['last_changed__max'] \
               or "1970-01-01T00:00+00:00"


class WarningComment(models.Model):
    comment = models.TextField(blank=True)
    warning = models.ForeignKey(Warning, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    last_changed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.comment

    @staticmethod
    def get_changes(id, changeTime="1970-01-01T00:00+00:00"):
        warning = Warning.objects.get(id=id)
        comments = WarningComment.objects.filter(warning=warning, last_changed__gt=changeTime).distinct().order_by(
            "time")
        return comments

    @property
    def html(self):
        return render_to_string("format/warning_comment.html", {"comment_id": self.id, "comment": self.comment,
                                                                   "time": self.time}).replace("\n", "")

    @staticmethod
    def get_max_time():
        return ContentComment.objects.all().aggregate(Max('last_changed'))['last_changed__max'] \
               or "1970-01-01T00:00+00:00"