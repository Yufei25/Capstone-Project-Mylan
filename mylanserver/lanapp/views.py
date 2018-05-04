# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from mimetypes import guess_type
from django.http import HttpResponse, Http404
from lanapp.models import *
from django.http import StreamingHttpResponse
from .search_algorithm import *


def index(request):
    contracts = Contract.objects.all()
    count = contracts.count()
    return render(request, 'index.html', {'count': count})


def search_portal(request):
    contracts = Contract.objects.all()
    count = contracts.count()
    return render(request, 'search.html', {'count': count})


def upload(request):
    return render(request, 'upload.html')


def upload_contract(request):
    for f in request.FILES.getlist('contracts'):
        new_contract = Contract(filename=f.name, contract=f)
        new_contract.save()
        get_title_and_paragraphs(new_contract)
    return redirect('show_contracts')
    # return redirect('test')


def get_title_and_paragraphs(contract):
    STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')
    document = Document(STATIC_ROOT + "/" + contract.contract.name)

    paras = []
    create_list = []
    for i in range(len(document.paragraphs)):

        p = document.paragraphs[i]
        paras.append(p)

        # create paragraph object
        if re.sub('\s|\xa0', '', p.text) == "":
            create_list.append(Paragraphs(index=i, contract=contract, text=paras[i].text, blankflag=True))
        else:
            create_list.append(Paragraphs(index=i, contract=contract, text=paras[i].text))
    Paragraphs.objects.bulk_create(create_list)

    # find contract title
    start_flag = False
    heading = ""
    for para in paras:
        if para.alignment == 1 and (not para.text.replace(u'\xa0', " ").lstrip() == ""):
            start_flag = True
            heading = heading + para.text + " "
        if (not para.alignment == 1) and start_flag == True:
            contract.title = heading
            contract.save()
            break


def show_contracts(request):
    contracts = Contract.objects.all()
    return render(request, 'view_files.html', {"contracts": contracts})


def delete_contract(request, id):
    contract = get_object_or_404(Contract, id=id)
    contract.delete()
    # contracts = Contract.objects.all()
    return redirect('show_contracts')


def delete_all_contract(request):
    contracts = Contract.objects.all()
    for contract in contracts:
        contract.delete()
    # contract = Contract.objects.all()
    return redirect('show_contracts')


def get_contract(request, id):
    contract = get_object_or_404(Contract, id=id)
    content_type = guess_type(contract.filename)
    return HttpResponse(contract.contract, content_type=content_type)


def key_search(request):
    if 'keyword' not in request.POST or not request.POST['keyword']:
        raise Http404
    else:

        keyword = request.POST['keyword']
        res_list = mylan_main_test(keyword)
        content_create_list = []
        warning_create_list = []
        for tuple in res_list:
            # filename = tuple[0]
            keyword = tuple[1]
            types = tuple[2]
            results = tuple[3]
            warnings = tuple[4]
            contract = tuple[5]
            # for result in results:
            #     if hasattr(result, '__iter__'):
            #         text = [paras.text.encode('ascii', 'ignore') for paras in result]
            #         res = "\n".join(text)

            #     else:
            #         res = result.text.encode('ascii', 'ignore')

            for warning in warnings:
                warning_create_list.append(Warning(warning=warning, contract=contract, keyword=keyword))
        Warning.objects.bulk_create(warning_create_list)

        context = {}
        contract_object = Contract.objects.all()
        first_contract = Contract.objects.all().first()
        content_object = Paragraphs.objects.filter(contract_id=first_contract.id)
        context['warnings']=Warning.objects.filter(contract_id=first_contract.id)
        context['contract_name'] = first_contract.filename
        context['contract_id'] = first_contract.id
        context['all_contracts'] = contract_object
        context['all_content'] = content_object

        warning_list = []
        for warning in context['warnings']:
            warning_list.append(warning.warning)
        context['all_warnings'] = list(set(warning_list))
        context['warning_count'] = len(context['all_warnings'])

        content_list =[]
        context['content_count'] = Content.objects.filter(contract_id=first_contract.id).count()
        return render(request, 'result.html', context)

def mylan_main_test(keyword):
    ########################################################################
    STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')
    # DIR = os.path.join(STATIC_ROOT, 'contracts').replace('\\', '/')
    # DIR2 = os.path.join(settings.MEDIA_ROOT, 'algorithm').replace('\\', '/')
    DIR2 = os.path.join(STATIC_ROOT, 'algorithm').replace('\\', '/')
    out_filename = 'Output_search.csv'
    out_path = os.path.join(DIR2, out_filename)
    stop_filename = os.path.join(DIR2 + '/res/', 'stop_words.txt')
    header = ['File Name', 'Keywords', 'Type', 'Content']  # Column names in output file
    ########################################################################

    res_list = []  # Input folder path
    # Write header
    with open(out_path, 'wb') as f:
        wr = csv.writer(f)
        wr.writerow(header)

    with open(out_path, 'ab') as f:

        stop_set = read_stop_words(stop_filename)

        contracts = Contract.objects.all()

        for contract in contracts:
            filename = contract.contract.name
            # Create a Document object of each of the files
            document = Document(STATIC_ROOT + "/" + filename)

            warning_list = []
            # search if there are tables containing keyword
            if not len(document.tables) == 0:
                if search_tables(document.tables, keyword, stop_set):
                    warning_list.append("Search term occur in tables")
                    print "Warning!! Search term occur in tables"

            # search if there are pictures
            if not len(document.inline_shapes) == 0:
                warning_list.append("Pictures in the document.")
                print "Warning!! pictures in the document"

            # A list to add all the paragraphs in the document
            paras = []

            '''
            The following for loop is used to add all the paragraphs in the document to the paras list object
            '''
            for i in range(len(document.paragraphs)):

                p = document.paragraphs[i]
                paras.append(p)

            # initial paragraph object and content object
            Paragraphs.objects.filter(contract=contract).update(highlight=False, endflag=False, warningflag=False, content=None)
            Content.objects.all().delete()

            paras_number = len(paras)  # Find the number of paragraphs in the document

            keywordindex, idx_to_term = search_2(paras, keyword, stop_set)

            results = []  # the list to output as the 'result' column in csv file
            keyword_lists = []  # the list to output as the 'keyword' column in csv file
            type_list = []  # the list to output as the 'type' column in csv file
            types = ["Heading", "Within content"]  # the two types of keywords

            lastendindex = 0

            for index in keywordindex:
                key = idx_to_term[index]

                # If the keyword is not at the start of a paragraph, just extract this paragraph and don't match
                # other paragraphs
                if not key.lower() in paras[index].text[:60 + len(key)].lower():
                    result = paras[index]
                    content = Content(content=paras[index].text, contract=contract, keyword=key, location="Within Content")
                    content.save()
                    endindex = index
                    type_flag = 1
                    mypara = Paragraphs.objects.get(index=index, contract=contract)
                    mypara.highlight = True
                    mypara.content = content
                    mypara.save()

                else:
                    type_flag = 0
                    target = find_patterns(paras, index, key, stop_set)  # Find the target pattern

                    if index == paras_number - 1:  # The last paragraph
                        result = paras[index]
                        mypara = Paragraphs.objects.get(index=index, contract=contract)
                        mypara.highlight = True
                        mypara.save()
                        endindex = index

                    else:
                        result, endindex = match(paras, target, index, stop_set, contract, lastendindex, key)

                if endindex > lastendindex:
                    keyword_lists.append(key)
                    results.append(result)
                    type_list.append(types[type_flag])
                    lastendindex = endindex

                    myparas = Paragraphs.objects.filter(index__lte=endindex, contract=contract).order_by('-index')
                    mypara = myparas.first()
                    mypara.endflag = True
                    mypara.save()

            # Output the result to a csv file
            wr = csv.writer(f)
            # Created a single list of all instances of 'Change of Control'
            # Ignored unrecognized ascii characters that throw an encoding error. Need improvement
            # for result in results:
            for i in range(len(results)):
                result = results[i]
                key = keyword_lists[i]
                mytype = type_list[i]
                if hasattr(result, '__iter__'):
                    text = [paras.text.encode('ascii', 'ignore') for paras in result]
                    res = "\n".join(text)
                else:
                    res = result.text.encode('ascii', 'ignore')

                wr.writerow([contract.filename, key.encode('ascii', 'ignore'), mytype, res])

            print '\n'
            res_list.append((contract.filename, keyword_lists, type_list, results, warning_list, contract))

    f.close()
    return res_list


def display(request, contractid):
    context = {}
    paras = Paragraphs.objects.filter(contract_id=contractid).order_by(index)
    context['paras'] = paras

    return render(request, 'lanapp/display.html', context)


def export(request):
    ########################################################################
    STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')
    DIR2 = os.path.join(STATIC_ROOT, 'algorithm').replace('\\', '/')
    out_filename = 'Output_search.csv'
    out_path = os.path.join(DIR2, out_filename)
    ########################################################################
    return download_file(out_path, out_filename)


def download_file(out_path, out_filename):
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(out_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(out_filename)

    return response


def get_contract_display(request):
    context = {}
    contract_object = Contract.objects.all()
    first_contract = Contract.objects.all().first()
    # print     contract_object.count()
    content_object = Paragraphs.objects.filter(contract_id=first_contract.id)
    context['contract_name'] = first_contract.filename
    context['contract_id'] = first_contract.id
    context['all_contracts'] = contract_object
    context['all_content'] = content_object

    warning_list = []
    for warning in context['warnings']:
        warning_list.append(warning.warning)
    context['all_warnings'] = list(set(warning_list))
    context['warning_count'] = len(context['all_warnings'])

    content_list = []
    context['content_count'] = Content.objects.filter(contract_id=current_contract.id).count()

    return render(request, 'result.html', context)


def get_current_contract(request, contract_id):
    context = {}
    contract_object = Contract.objects.all()
    current_contract = Contract.objects.get(id=contract_id)
    content_object = Paragraphs.objects.filter(contract_id=current_contract.id)
    context['warnings'] = Warning.objects.filter(contract_id=current_contract.id)
    current_list=[]
    for warning in context['warnings']:
        print warning.warning
        current_list.append(warning.warning)
    context['all_warnings'] = list(set(current_list))
    context['contract_name'] = current_contract.filename
    context['contract_id'] = current_contract.id
    context['all_contracts'] = contract_object
    context['all_content'] = content_object

    warning_list = []
    for warning in context['warnings']:
        warning_list.append(warning.warning)
    context['all_warnings'] = list(set(warning_list))
    context['warning_count'] = len(context['all_warnings'])

    content_list = []
    context['content_count'] = Content.objects.filter(contract_id=current_contract.id).count()
    return render(request, 'result.html', context)


def get_print_contract(request, contract_id):
    context = {}
    contract_object = Contract.objects.all()
    current_contract = Contract.objects.get(id=contract_id)
    content_object = Paragraphs.objects.filter(contract_id=current_contract.id)
    context['warnings'] = Warning.objects.filter(contract_id=current_contract.id)
    current_list=[]
    for warning in context['warnings']:
        print warning.warning
        current_list.append(warning.warning)
    context['all_warnings'] = list(set(current_list))
    context['contract_name'] = current_contract.filename
    context['contract_id'] = current_contract.id
    context['all_contracts'] = contract_object
    context['all_content'] = content_object

    warning_list = []
    for warning in context['warnings']:
        warning_list.append(warning.warning)
    context['all_warnings'] = list(set(warning_list))
    context['warning_count'] = len(context['all_warnings'])

    content_list = []
    context['content_count'] = Content.objects.filter(contract_id=current_contract.id).count()
    return render(request, 'print.html', context)


def about(request):
    return render(request, 'about.html', {})
