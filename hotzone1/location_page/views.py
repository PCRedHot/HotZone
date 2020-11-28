from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from hotzoneData.models import Place
from .forms import locationEditForm
import urllib.parse, requests
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def redirectView(request):
    res = redirect('/data/location/all/0')
    return res

@login_required
def deleteLocation(request, pk):
    location = Place.objects.get(pk=pk)
    location.delete()
    return redirect('/data/location/all/0')

@login_required
def locationSearch(request, offset):
    if 'location_search' not in request.GET:
        return redirectView(request)
    elif request.GET['location_search'] == '':
        return redirectView(request)
    q = request.GET['location_search']
    locationLoc = Place.objects.filter(location__icontains=q)
    locationAddress = Place.objects.filter(address__icontains=q)
    locationX = Place.objects.filter(x_coor__icontains=q)
    locationY = Place.objects.filter(y_coor__icontains=q)
    combined_location = locationLoc | locationAddress | locationX | locationY
    combined_location = combined_location.distinct().order_by('location')[offset*100:offset*100+100]
    context = {}
    context['location_list'] = combined_location
    context['offset'] = offset
    context['start_index'] = offset * 100 + 1
    context['end_index'] = offset * 100 + context['location_list'].count()
    context['previous'] = max(offset-1, 0)
    context['next'] = min(offset+1, (offset * 100 +context['location_list'].count())//100)
    context['q'] = q

    return render(request, 'location_search.html', context)

@login_required
def getEditLocation(request, pk):
    if request.method == 'GET':
        data = request.GET
        if not ('location' in data and 'address' in data and 'x' in data and 'y' in data):
            return HttpResponseRedirect('/data/location/all/0')
        place = Place.objects.get(pk=pk)
        place.location = data['location']
        place.address = data['address']
        place.x_coor = data['x']
        place.y_coor = data['y']
        place.save()
        return HttpResponseRedirect('/data/location/details/' + str(pk))
    else:
        form = locationEditForm(request.POST, pk=pk)
        if not form.is_valid():
            print('NOT VAILD')
            return HttpResponseRedirect('/data/location/all/0')
        place = Place.objects.get(pk=pk)
        place.location = form.cleaned_data['location']
        place.address = form.cleaned_data['address']
        place.x_coor = form.cleaned_data['x']
        place.y_coor = form.cleaned_data['y']
        place.save()
        return HttpResponseRedirect('/data/location/details/' + str(pk))

@login_required
def locationEditGeoDataView(request, pk):
    location = Place.objects.get(pk=pk)
    if ('location_query' in request.GET):
        query = request.GET['location_query']
        url = 'https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q=' + urllib.parse.quote(query).replace("%20", "+")
        res = requests.get(url)
        if res.status_code != 200:
            return render(request, 'location_add.html', { 'result_list': [], 'type': 1, 'res_code': res.status_code})
        context = {'pk': pk, 'type': 1, 'location': location}
        context['res_code'] = 200
        context['result_list'] = res.json()
        return render(request, 'location_add.html', context)
    else:
        return render(request, 'location_add.html', { 'result_list': [], 'type': 1, 'res_code': 200, 'location': location})

@login_required
def locationEditView(request, pk):
    context = {}
    context['location'] = Place.objects.get(pk=pk)
    context['form'] = locationEditForm(pk=pk)
    return render(request, 'location_edit.html', context)

@login_required
def getNewLocation(request):
    if request.method == 'GET':
        data = request.GET
        if not ('location' in data and 'address' in data and 'x' in data and 'y' in data):
            return HttpResponseRedirect('/data/location/all/0')
        place = Place.objects.create(location=data['location'], address=data['address'], x_coor=data['x'], y_coor=data['y'])
        return HttpResponseRedirect('/data/location/details/' + str(place.pk))
    return HttpResponseRedirect('/data/location/all/0')

@login_required
def locationNewView(request):
    if ('location_query' in request.GET):
        query = request.GET['location_query']
        url = 'https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q=' + urllib.parse.quote(query).replace("%20", "+")
        res = requests.get(url)
        if res.status_code != 200:
            return render(request, 'location_add.html', { 'result_list': [], 'type': 0, 'res_code': res.status_code})
        context = {}
        context['type'] = 0
        context['res_code'] = 200
        context['result_list'] = res.json()
        return render(request, 'location_add.html', context)
    else:
        return render(request, 'location_add.html', { 'result_list': [], 'type': 0, 'res_code': 200})

@login_required
def locationAllView(request, offset):
    context = {}
    context['location_list'] = Place.objects.order_by('location')[offset*100:offset*100+100]
    context['offset'] = offset
    context['start_index'] = offset * 100 + 1
    context['end_index'] = offset * 100 + context['location_list'].count()
    context['previous'] = max(offset-1, 0)
    context['next'] = min(offset+1,  (offset * 100 + context['location_list'].count())//100)
    return render(request, 'location.html', context)

@login_required
def locationDetailsView(request, pk):
    context = {}
    context = super().get_context_data(**kwargs)
    context['location'] = Place.objects.get(pk=pk)
    context['offset'] = (pk-1) // 100
    return render(request, 'location_details.html', context)
