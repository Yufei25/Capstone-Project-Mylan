# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse
from .search import *


def index(request):
    return HttpResponse("Hello, world. You're at the lanapp index.")


def test(request):
    str = '{0}&emsp;{1}&emsp;{2}<br/>'.format('File Name', 'Keywords', 'Content')
    res_list = mylan_main()

    for tuple in res_list:
        filename = tuple[0]
        keyword = tuple[1]
        results = tuple[2]
        for result in results:
            if hasattr(result, '__iter__'):
                text = [paras.text.encode('ascii', 'ignore') for paras in result]
                res = "<br/>".join(text)
            else:
                res = result.text.encode('ascii', 'ignore')

            str += '<br/>{0}&emsp;{1}&emsp;{2}<br/>'.format(filename, keyword, res)

        str += '<br/><br/><br/>-------------------------------------------------------------------------<br/>'
    return HttpResponse("Hello, world. You're testing!<br/>" + str)

