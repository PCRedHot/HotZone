from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from hotzoneData.models import Disease
from .forms import diseaseEditForm, diseaseAddForm

# Create your views here.
def redirectView(request):
    res = redirect('/data/disease/all/0')
    return res

def deleteDisease(request, pk):
    disease = Disease.objects.get(pk=pk)
    disease.delete()
    return redirect('/data/disease/all/0')

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

def diseaseEditView(request, pk):
    context = {}
    context['disease'] = Disease.objects.get(pk=pk)
    context['form'] = diseaseEditForm(pk=pk)

    return render(request, 'disease_edit.html', context)

def getNewDisease(request):
    if request.method == 'POST':
        form = diseaseAddForm(request.POST)
        if form.is_valid():
            disease = Disease.objects.create(disease_name=form.cleaned_data['disease_name'], virus=form.cleaned_data['virus'], max_infectious_period=form.cleaned_data['max_infectious_period'], curr_case_number=0)
            return HttpResponseRedirect('/data/disease/details/' + str(disease.pk))
    return HttpResponseRedirect('/data/disease/all/0')

def diseaseNewView(request):
    context = {}
    context['form'] = diseaseAddForm()

    return render(request, 'disease_add.html', context)

class diseaseAllView(TemplateView):
    template_name = "disease.html"

    def get_context_data(self, **kwargs):
        offset = self.kwargs['offset']

        context = super().get_context_data(**kwargs)
        context['disease_list'] = Disease.objects.order_by('disease_name')[offset*100:offset*100+100]
        context['offset'] = offset
        context['start_index'] = offset * 100 + 1
        context['end_index'] = offset * 100 + context['disease_list'].count()
        context['previous'] = max(offset-1, 0)
        context['next'] = min(offset+1,  (offset * 100 + context['disease_list'].count())//100)
        return context

class diseaseDetailsView(TemplateView):
    template_name = "disease_details.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']

        context = super().get_context_data(**kwargs)
        context['disease'] = Disease.objects.get(pk=pk)
        context['offset'] = pk // 100
        return context
