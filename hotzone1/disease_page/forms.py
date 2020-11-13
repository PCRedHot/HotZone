from django import forms
from hotzoneData.models import Disease
from django.forms import widgets

class diseaseEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        super(diseaseEditForm, self).__init__(*args, **kwargs)
        disease = Disease.objects.get(pk=pk)
        self.fields['disease_name'] = forms.CharField(max_length=20, initial=disease.disease_name)
        self.fields['virus'] = forms.CharField(max_length=20, initial=disease.virus)
        self.fields['max_infectious_period'] = forms.IntegerField(initial=disease.max_infectious_period)

class diseaseAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(diseaseAddForm, self).__init__(*args, **kwargs)
        self.fields['disease_name'] = forms.CharField(max_length=20)
        self.fields['virus'] = forms.CharField(max_length=20)
        self.fields['max_infectious_period'] = forms.IntegerField()
