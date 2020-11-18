from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from hotzoneData.models import *
from .forms import *
import urllib.parse, requests

# Create your views here.
@login_required
def redirectChooseDisease(request):
    return redirect('/data/case/disease/all/0')

@login_required
def chooseDiseaseView(request, offset):
    context = {}
    context['disease_list'] = Disease.objects.order_by('disease_name')[offset*100:offset*100+100]
    context['offset'] = offset
    context['start_index'] = offset * 100 + 1
    context['end_index'] = offset * 100 + context['disease_list'].count()
    context['previous'] = max(offset-1, 0)
    context['next'] = min(offset+1,  (offset * 100 + context['disease_list'].count())//100)
    return render(request, 'case_choose_disease.html', context)

@login_required
def chooseDiseaseSearchView(request, offset):
    if 'disease_search' not in request.GET:
        return redirectChooseDisease(request)
    elif request.GET['disease_search'] == '':
        return redirectChooseDisease(request)
    q = request.GET['disease_search']
    diseaseName = Disease.objects.filter(disease_name__icontains=q)
    diseaseVirus = Disease.objects.filter(virus__icontains=q)
    combined_disease = diseaseVirus | diseaseName
    combined_disease = combined_disease.distinct().order_by('disease_name')[offset*100:offset*100+100]
    context = {}
    context['disease_list'] = combined_disease
    context['offset'] = offset
    context['start_index'] = offset * 100 + 1
    context['end_index'] = offset * 100 + context['disease_list'].count()
    context['previous'] = max(offset-1, 0)
    context['next'] = min(offset+1, (offset * 100 +context['disease_list'].count())//100)
    context['q'] = q
    return render(request, 'case_choose_disease_search.html', context)

@login_required
def redirectDiseaseCase(request, pk):
    return redirect('/data/case/disease/'+ str(pk) +'/0')

@login_required
def diseaseCaseView(request, pk, offset):
    context = {}
    context['case_list'] = Case.objects.filter(disease_id=pk).order_by('case_number')[offset*100:offset*100+100]
    context['disease'] = Disease.objects.get(pk=pk)
    context['offset'] = offset
    context['start_index'] = offset * 100 + 1
    context['end_index'] = offset * 100 + context['case_list'].count()
    context['previous'] = max(offset-1, 0)
    context['next'] = min(offset+1, (offset * 100 +context['case_list'].count())//100)
    return render(request, 'case_disease.html', context)

@login_required
def diseaseCaseSearchView(request, pk, offset):
    if 'case_search' not in request.GET:
        return redirectDiseaseCase(request, pk)
    elif request.GET['case_search'] == '':
        return redirectDiseaseCase(request, pk)
    q = request.GET['case_search']
    allCase = Case.objects.filter(disease_id=pk)
    caseName = allCase.filter(patient__patient_name__icontains=q)
    caseId = allCase.filter(patient__identify_number__icontains=q)
    caseNumber = allCase.filter(pk__icontains=q)
    caseDate = allCase.filter(date_confirmed__icontains=q)
    combined_case = caseName | caseId | caseNumber | caseDate
    combined_case = combined_case.distinct().order_by('case_number')[offset*100:offset*100+100]
    context = {}
    context['disease'] = Disease.objects.get(pk=pk)
    context['case_list'] = combined_case
    context['offset'] = offset
    context['start_index'] = offset * 100 + 1
    context['end_index'] = offset * 100 + context['case_list'].count()
    context['previous'] = max(offset-1, 0)
    context['next'] = min(offset+1, (offset * 100 +context['case_list'].count())//100)
    context['q'] = q
    return render(request, 'case_disease_search.html', context)

@login_required
def getNewCase(request, pk):
    if request.method == 'POST':
        form = caseAddForm(request.POST)
        if not form.is_valid():
            return redirectDiseaseCase(request, pk)
        disease = Disease.objects.get(pk=pk)
        disease.curr_case_number += 1
        disease.save()
        case = Case.objects.create(case_number=disease.curr_case_number, disease=Disease.objects.get(pk=pk), patient=form.cleaned_data.get('patient'), date_confirmed=form.cleaned_data['date_confirmed'], is_local=form.cleaned_data['is_local'])
        return redirect('/data/case/details/'+str(case.pk))
    else:
        return redirectDiseaseCase(request, pk)

@login_required
def diseaseCaseAddView(request, pk):
    context = {
    'form': caseAddForm(),
    'disease': Disease.objects.get(pk=pk)
    }
    return render(request, 'case_disease_add.html', context)

@login_required
def caseDeleteView(request, pk):
    case = Case.objects.get(pk=pk)
    disease_pk = case.disease.pk
    case.delete()
    return redirect('/data/case/disease/' + str(disease_pk) + '/0')

@login_required
def caseDetailsView(request, pk):
    case = Case.objects.get(pk=pk)
    context = {
    'case': case,
    'offset': (case.case_number - 1) // 100,
    'location_list': CasePlace.objects.filter(case_id=pk)
    }
    return render(request, 'case_details.html', context)

@login_required
def locationDeleteView(request, pk):
    location = CasePlace.objects.get(pk=pk)
    case = location.case
    location.delete()
    return redirect('/data/case/details/' + str(case.pk))

def redirectLocationDetails(request, pk):
    return redirect('/data/case/location/details/' + str(pk))

@login_required
def getLocationEditView(request, pk):
    if request.method == 'POST':
        form = locationEditForm(request.POST, pk=pk)
        if not form.is_valid():
            return redirectLocationDetails(request, pk)
        location = CasePlace.objects.get(pk=pk)
        location.place = form.cleaned_data['location']
        location.category = form.cleaned_data['category']
        location.date_from = form.cleaned_data['date_from']
        location.date_to = form.cleaned_data['date_to']
        location.save()
        return redirectLocationDetails(request, pk)
    else:
        return redirectLocationDetails(request, pk)

@login_required
def locationEditView(request, pk):
    context = {
    'location': CasePlace.objects.get(pk=pk),
    'form': locationEditForm(pk=pk)
    }
    return render(request, 'case_location_edit.html', context)

@login_required
def locationDetailsView(request, pk):
    context = {
    'location': CasePlace.objects.get(pk=pk)
    }
    return render(request, 'case_location_details.html', context)

@login_required
def getNewPlace(request, pk):
    if request.method == 'GET':
        data = request.GET
        if not ('location' in data and 'address' in data and 'x' in data and 'y' in data):
            redirect('/data/case/location/details/add/query/'+str(pk))
        place = Place.objects.create(location=data['location'], address=data['address'], x_coor=data['x'], y_coor=data['y'])
        return redirect('/data/case/location/details/add/'+str(pk) + '?location_pk=' + str(place.pk))
    return redirect('/data/case/location/details/add/query/'+str(pk))

@login_required
def locationAddSearchView(request, pk):
    context = {
    'case': Case.objects.get(pk=pk),
    'res_code': 200
    }
    if ('location_query' in request.GET):
        query = request.GET['location_query']
        context['database_list'] = (Place.objects.filter(location__icontains=query) | Place.objects.filter(address__icontains=query)).distinct().order_by('location')
        url = 'https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q=' + urllib.parse.quote(query).replace("%20", "+")
        res = requests.get(url)
        if res.status_code != 200:
            context['res_code'] = res.status_code
            return render(request, 'case_location_add_search.html', context)
        context['result_list'] = res.json()
        return render(request, 'case_location_add_search.html', context)
    return render(request, 'case_location_add_search.html', context)

@login_required
def getLocationAddView(request, pk):
    if request.method == 'POST':
        if 'location_pk' not in request.GET:
            return redirect('/data/case/location/details/add/query/' + str(pk))
        form = locationAddForm(request.POST, location_pk=request.GET['location_pk'])
        if not form.is_valid():
            print(form.errors)
            return redirect('/data/case/location/details/add/query/' + str(pk))
        casePlace = CasePlace.objects.create(place=form.cleaned_data['location'], case=Case.objects.get(pk=pk), date_from=form.cleaned_data['date_from'], date_to=form.cleaned_data['date_to'], category=form.cleaned_data['category'])
        return redirect('/data/case/location/details/' + str(casePlace.pk))
    return redirect('/data/case/details/' + str(pk))

@login_required
def locationAddView(request, pk):
    if 'location_pk' not in request.GET:
         return redirect('/data/case/location/details/add/query/' + str(pk))
    location_pk = request.GET['location_pk']
    context = {
    'case': Case.objects.get(pk=pk),
    'form': locationAddForm(location_pk=location_pk),
    'location_pk': location_pk
    }
    return render(request, 'case_location_add.html', context)
