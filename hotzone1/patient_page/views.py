from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from hotzoneData.models import Patient
from .forms import patientEditForm, patientAddForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def redirectView(request):
    res = redirect('/data/patient/all/0')
    return res

@login_required
def deletePatient(request, pk):
    patient = Patient.objects.get(pk=pk)
    patient.delete()
    return redirect('/data/patient/all/0')

@login_required
def patientSearch(request, offset):
    if 'patient_search' not in request.GET:
        return redirectView(request)
    elif request.GET['patient_search'] == '':
        return redirectView(request)
    q = request.GET['patient_search']
    patientName = Patient.objects.filter(patient_name__icontains=q)
    patientId = Patient.objects.filter(identify_number__icontains=q)
    combined_patient = patientId | patientName
    combined_patient = combined_patient.distinct().order_by('patient_name')[offset*100:offset*100 + 100]
    context = {}
    context['patient_list'] = combined_patient
    context['offset'] = offset
    context['start_index'] = offset * 100 + 1
    context['end_index'] = offset * 100 + context['patient_list'].count()
    context['previous'] = max(offset-1, 0)
    context['next'] = min(offset+1, (offset * 100 +context['patient_list'].count())//100)
    context['q'] = q

    return render(request, 'patient_search.html', context)

@login_required
def getEditPatient(request, pk):
    if request.method == 'POST':
        form = patientEditForm(request.POST, pk=pk)
        if form.is_valid():
            patient = Patient.objects.get(pk=pk)
            patient.patient_name = form.cleaned_data['patient_name']
            patient.identify_number = form.cleaned_data['identify_number']
            patient.date_of_birth = form.cleaned_data['date_of_birth']
            patient.save()
            return HttpResponseRedirect('/data/patient/details/' + str(pk))
        else:
            return HttpResponseRedirect('/data/patient/details/edit/' + str(pk))
    else:
        return HttpResponseRedirect('/data/patient/all/0')

@login_required
def patientEditView(request, pk):
    context = {}
    context['patient'] = Patient.objects.get(pk=pk)
    context['form'] = patientEditForm(pk=pk)

    return render(request, 'patient_edit.html', context)

@login_required
def getNewPatient(request):
    if request.method == 'POST':
        form = patientAddForm(request.POST)
        if form.is_valid():
            patient = Patient.objects.create(patient_name=form.cleaned_data['patient_name'], identify_number=form.cleaned_data['identify_number'], date_of_birth=form.cleaned_data['date_of_birth'])
            return HttpResponseRedirect('/data/patient/details/' + str(patient.pk))
    return HttpResponseRedirect('/data/patient/all/0')

@login_required
def patientNewView(request):
    context = {}
    context['form'] = patientAddForm()

    return render(request, 'patient_add.html', context)

@login_required
def patientAllView(request, offset):
    context = {}
    context['patient_list'] = Patient.objects.order_by('patient_name')[offset*100:offset*100+100]
    context['offset'] = offset
    context['start_index'] = offset * 100 + 1
    context['end_index'] = offset * 100 + context['patient_list'].count()
    context['previous'] = max(offset-1, 0)
    context['next'] = min(offset+1,  (offset * 100 + context['patient_list'].count())//100)
    return render(request, 'patient.html', context)

@login_required
def patientDetailsView(request, pk):
    context = {}
    context['patient'] = Patient.objects.get(pk=pk)
    context['offset'] = pk // 100
    return render(request, 'patient_details.html', context)
