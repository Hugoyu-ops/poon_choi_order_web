from django.shortcuts import render, redirect
import os
from airtable import Airtable

AIRTABLE_MOVIESTABLE_BASE_ID = 'appHhDdwtwtYnJtFK'
AIRTABLE_API_KEY = 'key2fEpOGmPi9WJki'

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID', AIRTABLE_MOVIESTABLE_BASE_ID),
              'Table%201',
              api_key=os.environ.get('AIRTABLE_API_KEY', AIRTABLE_API_KEY))


# Create your views here.
def home(request):
    user_query = request.GET.get('query','')
    search = AT.get_all(formula="FIND('" + user_query + "', {Tel1})")
    date_query = str(request.GET.get('date_query'))
    date = AT.get_all(formula="FIND('" + date_query + "', {Dates})")
    context = {
        'search':search,
        'date': date,
    }
    return render(request, 'home.html', context)

def createoreder(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Tel1': request.POST.get('tel1'),
            'Tel2': request.POST.get('tel2'),
            'Districts': request.POST.get('district'),
            'Address': request.POST.get('address'),
            'Dates': request.POST.get('date'),
            'time': str(request.POST.get('time')),
            'AMPM': request.POST.get('AMPM'),
            'Quan': int(request.POST.get('quan')),
            'Price': int(request.POST.get('price')),
        }

        AT.insert(data)
    return redirect("/")

def detail(request, order_id):
    order = AT.get(order_id)
    return render(request, 'detail.html', order)

def edit(request, order_id):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Tel1': request.POST.get('tel1'),
            'Tel2': request.POST.get('tel2'),
            'Districts': request.POST.get('district'),
            'Address': request.POST.get('address'),
            'Dates': request.POST.get('date'),
            'time': str(request.POST.get('time')),
            'AMPM': request.POST.get('AMPM'),
            'Quan': int(request.POST.get('quan')),
            'Price': int(request.POST.get('price')),
            'Completed': request.POST.get('complete'),
        }

        AT.update(order_id, data)
    return redirect("/")

def delete(request, order_id):
    AT.delete(order_id)
    return redirect("/")

def search_by_date(request):
    if request.method == "GET":
        AT.get_all()
        date_query = str(request.GET.get('date_query'))
        date = AT.search('Dates', date_query)
        #date = date.id
        #date = AT.get_all(formula="FIND('" + date_query + "', {Dates})")
    return render(request, 'search_by_date.html', {'date':date})
