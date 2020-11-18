from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from hotzoneData.models import Disease
from .forms import diseaseEditForm, diseaseAddForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def redirectView(request):
    res = redirect('/data/disease/all/0')
    return res

@login_required
def deleteDisease(request, pk):
    disease = Disease.objects.get(pk=pk)
    disease.delete()
    return redirect('/data/disease/all/0')

@login_required
def diseaseSearch(request, offset):
    if 'disease_search' not in request.GET:
        return redirectView(request)
    elif request.GET['disease_search'] == '':
        return redirectView(request)
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
    return render(request, 'disease_search.html', context)

@login_required
def getEditDisease(request, pk):
    if request.method == 'POST':
        form = diseaseEditForm(request.POST, pk=pk)
        if form.is_valid():
            disease = Disease.objects.get(pk=pk)
            disease.disease_name = form.cleaned_data['disease_name']
            disease.virus = form.cleaned_data['virus']
            disease.max_infectious_period = form.cleaned_data['max_infectious_period']
            disease.save()
            return HttpResponseRedirect('/data/disease/details/' + str(pk))
        else:
            return HttpResponseRedirect('/data/disease/details/edit/' + str(pk))
    else:
        return HttpResponseRedirect('/data/disease/all/0')

@login_required
def diseaseEditView(request, pk):
    context = {}
    context['disease'] = Disease.objects.get(pk=pk)
    context['form'] = diseaseEditForm(pk=pk)

    return render(request, 'disease_edit.html', context)

@login_required
def getNewDisease(request):
    if request.method == 'POST':
        form = diseaseAddForm(request.POST)
        if form.is_valid():
            disease = Disease.objects.create(disease_name=form.cleaned_data['disease_name'], virus=form.cleaned_data['virus'], max_infectious_period=form.cleaned_data['max_infectious_period'], curr_case_number=0)
            return HttpResponseRedirect('/data/disease/details/' + str(disease.pk))
    return HttpResponseRedirect('/data/disease/all/0')

@login_required
def diseaseNewView(request):
    context = {}
    context['form'] = diseaseAddForm()

    return render(request, 'disease_add.html', context)

@login_required
def diseaseAllView(request, offset):
    context = {}
    context['disease_list'] = Disease.objects.order_by('disease_name')[offset*100:offset*100+100]
    context['offset'] = offset
    context['start_index'] = offset * 100 + 1
    context['end_index'] = offset * 100 + context['disease_list'].count()
    context['previous'] = max(offset-1, 0)
    context['next'] = min(offset+1,  (offset * 100 + context['disease_list'].count())//100)
    return render(request, 'disease.html', context)

@login_required
def diseaseDetailsView(request, pk):
    context = {}
    context['disease'] = Disease.objects.get(pk=pk)
    context['offset'] = pk // 100
    return render(request, 'disease_details.html', context)
