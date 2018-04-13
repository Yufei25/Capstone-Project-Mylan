# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from mimetypes import guess_type
from django.http import HttpResponse, Http404
from lanapp.forms import *
from django.http import StreamingHttpResponse
from .search_algorithm import *


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
    # contracts = Contract.objects.all()
    return redirect('show_contracts')


def delete_all_contract(request):
    Contract.objects.all().delete()
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


def mylan_main_test(keyword):
    ########################################################################
    STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')
    DIR = os.path.join(STATIC_ROOT, 'contracts').replace('\\', '/')

    DIR2 = os.path.join(STATIC_ROOT, 'algorithm').replace('\\', '/')
    out_filename = 'Output_search.csv'
    out_path = os.path.join(DIR2, out_filename)
    stop_filename = os.path.join(DIR2 + '/res/', 'stop_words.txt')
    header = ['File Name', 'Keywords', 'Content']  # Column names in output file
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
            filename = contract.filename
            # Create a Document object of each of the files
            document = Document(DIR + "/" + filename)

            # search if there are tables containing keyword
            if not len(document.tables) == 0:
                if search_tables(document.tables, keyword, stop_set):
                    print("Exception!! Keywords occur in tables")

            # search if there are pictures
            if not len(document.inline_shapes) == 0:
                print("Exception!! pictures in the document")

            # A list to add all the paragraphs in the document
            paras = []

            '''
            The following for loop is used to add all the paragraphs in the document to the paras list object
            '''
            for p in document.paragraphs:
                # print(p.text)
                paras.append(p)

            paras_number = len(paras)  # Find the number of paragraphs in the document

            keywordindex, idx_to_term = search_2(paras, keyword, stop_set)

            results = []
            keyword_lists = []

            # find contract name
            start_flag = False
            heading = ""
            for para in paras:
                # print para.alignment
                if para.alignment == 1 and (not para.text.replace(u'\xa0', " ").lstrip() == ""):
                    start_flag = True
                    heading = heading + para.text + " "
                if (not para.alignment == 1) and start_flag == True:
                    print "Contract heading: " + heading
                    break
            lastendindex = 0
            endindex = 0  # The index of the end of the last matched content

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
                    # print '\tTarget Paragraph: [{0}]\n\t\t{1}\n'.format(index, paras[index].text.encode("utf-8"))

                else:
                    # print '\tTarget Paragraph: [{0}]\n\t\t{1}\n'.format(index, paras[index].text.encode("utf-8"))
                    target = find_patterns(paras, index, keyword, stop_set)  # Find the target pattern

                    if index == paras_number - 1:  # The last paragraph
                        result = paras[index]
                    else:
                        result, endindex = match(paras, target, index, stop_set)

                if endindex > lastendindex:
                    keyword_lists.append(keyword)
                    results.append(result)
                    lastendindex = endindex

            # Output the result to a csv file
            wr = csv.writer(f)
            # Created a single list of all instances of 'Change of Control'
            # Ignored unrecognized ascii characters that throw an encoding error. Need improvement
            # for result in results:
            for i in range(len(results)):
                result = results[i]
                keyword = keyword_lists[i]
                if hasattr(result, '__iter__'):
                    text = [paras.text.encode('ascii', 'ignore') for paras in result]
                    res = "\n".join(text)
                else:
                    res = result.text.encode('ascii', 'ignore')

                wr.writerow([filename, keyword, res])

            print '\n'
            res_list.append((filename, keyword, results))

    f.close()
    return res_list


def display(request):
    context = {}
    results = SearchResult.objects.all()
    context['results'] = results

    return render(request, 'display.html', context)


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
    Contract.objects.all().delete()
    SearchResult.objects.all().delete()
