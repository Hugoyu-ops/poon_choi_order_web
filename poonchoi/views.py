from django.shortcuts import render, redirect
import os
from airtable import Airtable
from django.http import HttpResponseRedirect


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID', AIRTABLE_MOVIESTABLE_BASE_ID),
              'Table%201',
              api_key=os.environ.get('AIRTABLE_API_KEY', AIRTABLE_API_KEY))


# Create your views here.
def home(request):
    user_query = request.GET.get('query','')
    search = AT.get_all(formula="FIND('" + user_query + "', {Tel1})", sort='Dates')
    date_query = str(request.GET.get('date_query'))
    date = AT.get_all(formula="FIND('" + date_query + "', {Dates})")
    context = {
        'search':search,
        'date': date,
    }
    return render(request, 'home.html', context)

def completed(request):
    user_query = request.GET.get('query','')
    search = AT.get_all(formula="FIND('" + user_query + "', {Tel1})", sort='Dates')
    date_query = str(request.GET.get('date_query'))
    date = AT.get_all(formula="FIND('" + date_query + "', {Dates})")
    context = {
        'search':search,
        'date': date,
    }
    return render(request, 'completed.html', context)

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


# edit button on home page
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
    return redirect('/')

# edit button on search by date page
def edit_on_date(request, order_id):
    if request.method == 'POST':
        date_para = AT.get(order_id)['fields'].get('Dates')
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
    return redirect('/Date/?date_query='+date_para)

def edit_on_date_completed(request, order_id):
    if request.method == 'POST':
        date_para = AT.get(order_id)['fields'].get('Dates')
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
    return redirect('/Date_completed/?date_query='+date_para)

def edit_completed(request, order_id):
    if request.method == 'POST':
        date_para = AT.get(order_id)['fields'].get('Dates')
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
    return redirect('/completed')

def delete(request, order_id):
    AT.delete(order_id)
    return redirect("/")

def completed_delete(request, order_id):
    AT.delete(order_id)
    return redirect("/completed")

def delete_on_date(request, order_id):
    date_para = AT.get(order_id)['fields'].get('Dates')
    AT.delete(order_id)
    return redirect('/Date/?date_query='+date_para)

def completed_delete_on_date(request, order_id):
    date_para = AT.get(order_id)['fields'].get('Dates')
    AT.delete(order_id)
    return redirect('/Date_completed/?date_query='+date_para)

def search_by_date(request):
    if request.method == "GET":
        amount = [0]
        am = [0]
        pm = [0]
        sp_am =[0]
        sp_pm =[0]
        not_confirm = [0]
        sp_not_confirm = [0]
        #AT.get_all()
        date_query = str(request.GET.get('date_query', ''))
        #date = AT.search('Dates', date_query)
        date = AT.get_all(formula="FIND('" + date_query + "', {Dates})", sort=['AMPM', 'time'])
        for order in date:
            amount.append(int(order['fields']['total_price']))
            total_amount = sum(amount)
        for order in date:
            if 'Districts' in order['fields']:
                if order['fields']['Districts'] != '自取':
                    if 'AMPM' in order['fields']:
                        if order['fields']['AMPM'] == "AM":
                            am.append(int(order['fields']['Quan']))
                        else:
                            pm.append(int(order['fields']['Quan']))
                    else:
                        not_confirm.append(int(order['fields']['Quan']))
                else:
                    if 'AMPM' in order['fields']:
                        if order['fields']['AMPM'] == "AM":
                            sp_am.append(int(order['fields']['Quan']))
                        else:
                            sp_pm.append(int(order['fields']['Quan']))
                    else:
                        sp_not_confirm.append(int(order['fields']['Quan']))

        if len(am) > 0:
            am_quan = str(sum(am))
        else:
            am_quan = '0'

        if len(pm) > 0:
             pm_quan = str(sum(pm))
        else:
            pm_quan = '0'

        if len(sp_am) > 0:
            sp_am_quan =str(sum(sp_am))
        else:
            sp_am_quan = '0'

        if len(sp_pm) > 0:
            sp_pm_quan =str(sum(sp_pm))
        else:
            sp_pm_quan = '0'

        if len(sp_not_confirm) > 0:
            sp_not_confirm_quan = str(sum(sp_not_confirm))
        else:
            sp_not_confirm_quan = '0'

        if len(not_confirm) > 0:
            not_confirm_quan = str(sum(not_confirm))
        else:
            not_confirm_quan ='0'

        context = {
            'total_amount': total_amount,
            'date': date,
            'am_quan': am_quan,
            'pm_quan': pm_quan,
            'not_confirm_quan': not_confirm_quan,
            'sp_am_quan':sp_am_quan,
            'sp_pm_quan':sp_pm_quan,
            'sp_not_confirm_quan':sp_not_confirm_quan
        }

    return render(request, 'search_by_date.html', context)

def completed_by_date(request):
    if request.method == "GET":
        #AT.get_all()
        date_query = str(request.GET.get('date_query', ''))
        #date = AT.search('Dates', date_query)
        date = AT.get_all(formula="FIND('" + date_query + "', {Dates})", sort=['AMPM', 'time'])

        context = {
            'date': date,
        }

    return render(request, 'completed_by_date.html', context)