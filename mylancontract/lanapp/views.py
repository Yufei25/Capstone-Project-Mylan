# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect,get_object_or_404
from mimetypes import guess_type
from django.http import HttpResponse, Http404
from lanapp.forms import *

from .search import *


def index(request):
    return render(request, 'index.html', {})


def search_portal(request):
    return render(request, 'search.html', {})


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


def upload(request):
    return render(request, 'upload.html')


def upload_contract(request):
    for f in request.FILES.getlist('contracts'):
        new_contract = Contract(filename=f.name, contract=f)
        new_contract.save()
    return redirect('show_contracts')

def show_contracts(request):
    contracts = Contract.objects.all()
    return render(request, 'view_files.html', {"contracts": contracts})


def delete_contract(request, id):
    contract = get_object_or_404(Contract, id=id)
    contract.delete()  
    contracts = Contract.objects.all()
    return redirect('show_contracts')

def delete_all_contract(request):
    Contract.objects.all().delete()
    contract = Contract.objects.all()
    return redirect('show_contracts')


def get_contract(request, id):
    contract = get_object_or_404(Contract, id=id)
    content_type = guess_type(contract.filename)
    return HttpResponse(contract.contract, content_type=content_type)


def key_search(request):
    context = {}
    if 'keyword' not in request.POST or not request.POST['keyword']:
        raise Http404
    else:
        clean_data()

        keyword = request.POST['keyword']
        res_list = mylan_main(keyword)
        for tuple in res_list:
            filename = tuple[0]
            keyword = tuple[1]
            results = tuple[2]
            for result in results:
                if hasattr(result, '__iter__'):
                    text = [paras.text.encode('ascii', 'ignore') for paras in result]
                    res = "\n".join(text)

                else:
                    res = result.text.encode('ascii', 'ignore')

                search_result = SearchResult.objects.create(filename=filename, keyword=keyword, content=res)
                search_result.save()

        results = SearchResult.objects.all()
        context['results'] = results

        return render(request, 'display.html', context)


def display(request):
    context = {}
    results = SearchResult.objects.all()
    context['results'] = results

    return render(request, 'display.html', context)


def export(request):
    return HttpResponse("Hello! You're on Export Page!<br/>")


def clean(request):
    return HttpResponse("Hello! You're on Clean Page!<br/>")


def clean_data():
    SearchResult.objects.all().delete()
