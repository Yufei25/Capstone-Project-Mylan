# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from mimetypes import guess_type
from django.http import HttpResponse, Http404
from lanapp.forms import *
from django.http import StreamingHttpResponse
from .search_algorithm import *



def index(request):
    return render(request, 'lanapp/index.html', {})


def search_portal(request):
    return render(request, 'lanapp/search.html', {})


# def test(request):
#     str = '{0}&emsp;{1}&emsp;{2}<br/>'.format('File Name', 'Keywords', 'Content')
#     res_list = mylan_main()
#
#     for tuple in res_list:
#         filename = tuple[0]
#         keyword = tuple[1]
#         results = tuple[2]
#         for result in results:
#             if hasattr(result, '__iter__'):
#                 text = [paras.text.encode('ascii', 'ignore') for paras in result]
#                 res = "<br/>".join(text)
#             else:
#                 res = result.text.encode('ascii', 'ignore')
#
#             str += '<br/>{0}&emsp;{1}&emsp;{2}<br/>'.format(filename, keyword, res)
#
#         str += '<br/><br/><br/>-------------------------------------------------------------------------<br/>'
#     return HttpResponse("Hello, world. You're testing!<br/>" + str)


def upload(request):
    return render(request, 'lanapp/upload.html')


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
    for i in range(len(document.paragraphs)):

        p = document.paragraphs[i]
        paras.append(p)

        # create paragraph object
        if re.sub('\s|\xa0','',p.text)  == "":
            continue
        mypara = Paragraphs.objects.create(index=i, contract=contract, content=paras[i].text, highlight=False, endflag= False)
        mypara.save()

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
    return render(request, 'lanapp/view_files.html', {"contracts": contracts})


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
    context = {}
    if 'keyword' not in request.POST or not request.POST['keyword']:
        raise Http404
    else:
        SearchResult.objects.all().delete()

        keyword = request.POST['keyword']
        res_list = mylan_main_test(keyword)
        for tuple in res_list:
            # filename = tuple[0]
            keyword = tuple[1]
            types = tuple[2]
            results = tuple[3]
            warnings = tuple[4]
            contract = tuple[5]
            for result in results:
                if hasattr(result, '__iter__'):
                    text = [paras.text.encode('ascii', 'ignore') for paras in result]
                    res = "\n".join(text)

                else:
                    res = result.text.encode('ascii', 'ignore')

                # search_result = SearchResult.objects.create(filename=filename, keyword=keyword, content=res)
                # search_result.save()

                # testing part
                content = Content.objects.create(content=res, contract=contract, keyword=keyword)
                content.save()
            for warning in warnings:
                warning = Warning.objects.create(warning=warning, contract=contract, keyword=keyword)
                warning.save()

        # results = SearchResult.objects.all()
        # context['results'] = results

        # return render(request, 'lanapp/display.html', context)
        return redirect('test')


def mylan_main_test(keyword):
    ########################################################################
    STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')
    #DIR = os.path.join(STATIC_ROOT, 'contracts').replace('\\', '/')

    DIR2 = os.path.join(STATIC_ROOT, 'algorithm').replace('\\', '/')
    out_filename = 'Output_search.csv'
    out_path = os.path.join(DIR2, out_filename)
    stop_filename = os.path.join(DIR2 + '/res/', 'stop_words.txt')
    header = ['File Name', 'Keywords','Type', 'Content']  # Column names in output file
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
                    warning_list.append("Keywords occur in tables")
                    print "Warning!! Keywords occur in tables"

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
            #for p in document.paragraphs:
                # print(p.text)
                p = document.paragraphs[i]
                paras.append(p)

            # initial paragraph object
            myparas = Paragraphs.objects.filter(contract=contract)
            for mypara in myparas:
                mypara.highlight = False
                mypara.endflag = False
                mypara.save()
            

            paras_number = len(paras)  # Find the number of paragraphs in the document

            keywordindex, idx_to_term = search_2(paras, keyword, stop_set)

            results = [] # the list to output as the 'result' column in csv file
            keyword_lists = [] # the list to output as the 'keyword' column in csv file
            type_list = []  # the list to output as the 'type' column in csv file
            types = ["Heading", "Within content"]   # the two types of keywords

            
            lastendindex = 0
            endindex = 0  # The index of the end of the last matched content
            
            # indicate the type of the keyword. 0 = heading, 1 = within content 
            type_flag = 0  

            for index in keywordindex:
                keyword = idx_to_term[index]
                # If the paragraph has been matched before, ignore it
                # if index <= endindex:
                #     continue

                # If the keyword is not at the start of a paragraph, just extract this paragraph and don't match
                # other paragraphs
                if not keyword.lower() in paras[index].text[:60 + len(keyword)].lower():
                    result = paras[index]
                    endindex = index
                    type_flag = 1
                    mypara = Paragraphs.objects.get(index=index, contract=contract)
                    mypara.highlight = True
                    mypara.save()
                    
                    # print '\tTarget Paragraph: [{0}]\n\t\t{1}\n'.format(index, paras[index].text.encode("utf-8"))

                else:
                    type_flag = 0
                    # print '\tTarget Paragraph: [{0}]\n\t\t{1}\n'.format(index, paras[index].text.encode("utf-8"))
                    target = find_patterns(paras, index, keyword, stop_set)  # Find the target pattern

                    if index == paras_number - 1:  # The last paragraph
                        result = paras[index]
                        mypara = Paragraphs.objects.get(index=index, contract=contract)
                        mypara.highlight = True
                        mypara.save()
                        endindex = index

                    else:
                        result, endindex = match(paras, target, index, stop_set, contract)

                if endindex > lastendindex:
                    keyword_lists.append(keyword)
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
                keyword = keyword_lists[i]
                mytype = type_list[i]
                if hasattr(result, '__iter__'):
                    text = [paras.text.encode('ascii', 'ignore') for paras in result]
                    res = "\n".join(text)
                else:
                    res = result.text.encode('ascii', 'ignore')

                wr.writerow([contract.filename, keyword,mytype, res])

            print '\n'
            res_list.append((contract.filename, keyword_lists, type_list, results, warning_list, contract))

    f.close()
    return res_list


def display(request, contractid):
    context = {}
    paras = Paragraphs.objects.all().filter(contract_id=contractid).order_by(index)
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
    # return HttpResponse("Hello! You're on Export Page!<br/>")


def clean(request):
    clean_data()
    return HttpResponse("Hello! You're on Clean Page!<br/>")


def clean_data():
    contracts = Contract.objects.all()
    for contract in contracts:
        contract.delete()
    SearchResult.objects.all().delete()


def test(request):
    contracts = Contract.objects.all()
    return render(request, 'lanapp/test.html', {"contracts": contracts})


def contract_comment(request, contract_id):
    if not 'comment' in request.POST or not request.POST['comment']:
        # print('testing view.py! 404')
        raise Http404
    else:
        context = {}

        # Creates a bound form from the request POST parameters and makes the
        # form available in the request context dictionary.
        form = ContractCommentForm(request.POST)
        context['commentform'] = form

        # Validates the form.
        if not form.is_valid():
            raise Http404
            # https://stackoverflow.com/questions/12758786/redirect-return-to-same-previous-page-in-django
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'), context)
            # return HttpResponse("")  # Empty response on success.

        contract = get_object_or_404(Contract, id=contract_id)

        commenttext = form.cleaned_data['comment']

        new_comment = ContractComment(comment=commenttext, contract=contract)
        new_comment.save()

        comments = ContractComment.objects.filter(contract=contract).order_by("time")
        context['contract_comments'] = comments

        return render(request, 'format/contract_comments.json', context, content_type='application/json')


def content_comment(request, content_id):
    if not 'comment' in request.POST or not request.POST['comment']:
        raise Http404
    else:
        context = {}

        # Creates a bound form from the request POST parameters and makes the
        # form available in the request context dictionary.
        form = ContentCommentForm(request.POST)
        context['commentform'] = form

        # Validates the form.
        if not form.is_valid():
            raise Http404
            # https://stackoverflow.com/questions/12758786/redirect-return-to-same-previous-page-in-django
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'), context)
            # return HttpResponse("")  # Empty response on success.

        content = get_object_or_404(Content, id=content_id)

        commenttext = form.cleaned_data['comment']

        new_comment = ContentComment(comment=commenttext, content=content)
        new_comment.save()

        comments = ContentComment.objects.filter(content=content).order_by("time")
        context['content_comments'] = comments

        return render(request, 'format/content_comments.json', context, content_type='application/json')


def warning_comment(request, warning_id):
    if not 'comment' in request.POST or not request.POST['comment']:
        raise Http404
    else:
        context = {}

        # Creates a bound form from the request POST parameters and makes the
        # form available in the request context dictionary.
        form = WarningCommentForm(request.POST)
        context['commentform'] = form

        # Validates the form.
        if not form.is_valid():
            raise Http404
            # https://stackoverflow.com/questions/12758786/redirect-return-to-same-previous-page-in-django
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'), context)
            # return HttpResponse("")  # Empty response on success.

        warning = get_object_or_404(Warning, id=warning_id)

        commenttext = form.cleaned_data['comment']

        new_comment = WarningComment(comment=commenttext, warning=warning)
        new_comment.save()

        comments = WarningComment.objects.filter(warning=warning).order_by("time")
        context['warning_comments'] = comments
        return render(request, 'format/warning_comments.json', context, content_type='application/json')


@transaction.atomic
def get_contract_comments_changes(request, contract_id, time="1970-01-01T00:00+00:00"):
    if time == 'undefined' or time == '':
        time = "1970-01-01T00:00+00:00"
    max_time = ContractComment.get_max_time()
    contract_comments = ContractComment.get_changes(contract_id, time)
    context = {"max_time": max_time, "contract_comments": contract_comments}
    return render(request, 'format/contract_comments.json', context, content_type='application/json')


@transaction.atomic
def get_content_comments_changes(request, content_id, time="1970-01-01T00:00+00:00"):
    if time == 'undefined' or time == '':
        time = "1970-01-01T00:00+00:00"
    max_time = ContentComment.get_max_time()
    content_comments = ContentComment.get_changes(content_id, time)
    context = {"max_time": max_time, "content_comments": content_comments}
    return render(request, 'format/content_comments.json', context, content_type='application/json')


@transaction.atomic
def get_warning_comments_changes(request, warning_id, time="1970-01-01T00:00+00:00"):
    if time == 'undefined' or time == '':
        time = "1970-01-01T00:00+00:00"
    max_time = WarningComment.get_max_time()
    warning_comments = WarningComment.get_changes(warning_id, time)
    context = {"max_time": max_time, "warning_comments": warning_comments}
    return render(request, 'format/warning_comments.json', context, content_type='application/json')


@transaction.atomic
def get_contents_changes(request, contract_id, time="1970-01-01T00:00+00:00"):
    if time == 'undefined' or time == '':
        time = "1970-01-01T00:00+00:00"
    max_time = Content.get_max_time()
    contents = Content.get_changes(contract_id, time)
    context = {"max_time": max_time, "contents": contents}
    return render(request, 'format/contents.json', context, content_type='application/json')


@transaction.atomic
def get_warnings_changes(request, contract_id, time="1970-01-01T00:00+00:00"):
    if time == 'undefined' or time == '':
        time = "1970-01-01T00:00+00:00"
    max_time = Warning.get_max_time()
    warnings = Warning.get_changes(contract_id, time)
    context = {"max_time": max_time, "warnings": warnings}
    return render(request, 'format/warnings.json', context, content_type='application/json')


# Returns all recent changes to the database, as JSON
@transaction.atomic
def get_changes(request, time="1970-01-01T00:00+00:00"):
    if time == 'undefined' or time == '':
        time = "1970-01-01T00:00+00:00"
    max_time = Contract.get_max_time()
    contracts = Contract.get_changes(time)
    context = {"max_time": max_time, "contracts": contracts}
    return render(request, 'format/contracts.json', context, content_type='application/json')
