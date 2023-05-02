from django.http import HttpResponse
from django.shortcuts import render
import os
import json
from django.urls import reverse
import pandas as pd
from django.http import FileResponse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')
    
def contact(request):
    return render(request, 'contact.html')
        
def browse(request):
    df = pd.read_csv("/home/maahistory/public_html/test_project/static/docsv.csv")
    json_records = df.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}
    return render(request, "browse.html", context)
    
    
def Search(request):
    df = df = pd.concat(
    map(pd.read_csv, ["/home/maahistory/public_html/test_project/static/amm-sampled-metadata.csv",
     "/home/maahistory/public_html/test_project/static/Sampled-MetaData-IndianSection.csv"]), ignore_index=True)

    df = df.applymap(str)
    # parsing the DataFrame in json format.

    
    if 'q' in request.GET:
        q = request.GET['q']
        if q == '':
            print("No query found")
        else:
            print(q)
            p = '|'.join(q.split())
            res = df[df['title'].str.contains(p, case=False)]
            df = res

    else:
        print("rendering a default view")

    if 'y' in request.GET:
        y = request.GET['y']
        if y == '':
            print("No date query found")
        else:
            res = df[df['publicationYear'] >= y]
            df = res
            print("Sorted date with query")
    else:
        print("rendering date default view")

    if 'y2' in request.GET:
        y2 = request.GET['y2']
        if y2 == '':
            print("No date query found")
        else:
            res = df[df['publicationYear'] <= y2]
            df = res
            print("Sorted date with query")
    else:
        print("rendering date default view")

    if 'v' in request.GET:
        v = request.GET['v']
        if v == '':
            print("No volume query found")
        else:
            res = df[df['volumeNumber'].str.contains(v, case=False)]
            df = res
            print("Sorted volume with query")
    else:
        print("rendering volume default view")

    if 'sort' in request.GET:
        sort = request.GET['sort']
        if sort == '':
            print("No sort order found")
        elif sort == 'Old':
            print("Sorting Old to New")
            df = df.sort_values(by=['publicationYear'], ascending=True)
        elif sort == 'New':
            print("Sorting New to Old")
            df = df.sort_values(by=['publicationYear'], ascending=False)
        elif sort == 'AZ':
            print("Sorting A to Z")
            df = df.sort_values(by=['title'], ascending=True)
        elif sort == 'ZA':
            print("Sorting Z to A")
            df = df.sort_values(by=['title'], ascending=False)
        elif sort == "Rel" and 'q' in request.GET:
            if 'q' in request.GET:
                q = request.GET['q']
                
                keywords = q.lower().split()

                # sum keywords in each title case-insensitive
                def count_matching_keywords(text):
                    return sum(1 for keyword in keywords if keyword in text.lower().split())

                # apply function to create new column with count of matching keywords
                df['matching_keywords'] = df['title'].apply(count_matching_keywords)

                # sort DataFrame by number of matching keywords in descending order
                df = df.sort_values(by='matching_keywords', ascending=False)

                # print statement for debugging
                # with pd.option_context('display.max_rows', None, 'display.max_columns',
                #                       None):  # more options can be specified also
                #    print(df[['title','matching_keywords']])

                # remove temporary column
                df = df.drop('matching_keywords', axis=1)
                print("Sorted by Relevancy")

        else:
            print("rendering with default sort")
            df = df.sort_values(by=['publicationYear'], ascending=True)
    else:
        df = df.sort_values(by=['publicationYear'], ascending=True)


    json_records = df.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data, 'n': len(data)}
    return render(request, 'search.html', context)
    
    
def show_pdf(request,f,p,doc):
    return FileResponse(open('/home/maahistory/public_html/test_project/' + f + '/' + p + '/' + doc, 'rb'), content_type='application/pdf')