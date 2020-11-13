from django import forms
from hotzoneData.models import Patient
from django.forms import widgets
import datetime

class patientEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        super(patientEditForm, self).__init__(*args, **kwargs)
        patient = Patient.objects.get(pk=pk)
        self.fields['patient_name'] = forms.CharField(max_length=100, initial=patient.patient_name)
        self.fields['identify_number'] = forms.CharField(max_length=20, initial=patient.identify_number)
        self.fields['date_of_birth'] = forms.DateField(initial=patient.date_of_birth, input_formats=['%Y-%m-%d'])

class patientAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(patientAddForm, self).__init__(*args, **kwargs)
        self.fields['patient_name'] = forms.CharField(max_length=100)
        self.fields['identify_number'] = forms.CharField(max_length=20)
        self.fields['date_of_birth'] = forms.DateField(input_formats=['%Y-%m-%d'])
