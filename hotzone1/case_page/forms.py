from django import forms
from hotzoneData.models import *
from django.forms import widgets
import datetime

class caseAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(caseAddForm, self).__init__(*args, **kwargs)
        self.fields['patient'] = forms.ModelChoiceField(queryset=Patient.objects.order_by('patient_name'))
        self.fields['date_confirmed'] = forms.DateField(initial=datetime.date.today(), input_formats=['%Y-%m-%d'])
        self.fields['is_local'] = forms.BooleanField(initial=True, required=False)

class locationEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        super(locationEditForm, self).__init__(*args, **kwargs)
        location = CasePlace.objects.get(pk=pk)
        self.fields['location'] = forms.ModelChoiceField(queryset=Place.objects.order_by('location'), initial=location.place)
        self.fields['category'] = forms.ChoiceField(choices=CasePlace.CAT_CHOICES, initial=location.category)
        self.fields['date_from'] = forms.DateField(initial=location.date_from, input_formats=['%Y-%m-%d'])
        self.fields['date_to'] = forms.DateField(initial=location.date_to, input_formats=['%Y-%m-%d'])

class locationAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        location_pk = kwargs.pop('location_pk')
        super(locationAddForm, self).__init__(*args, **kwargs)
        location = Place.objects.get(pk=location_pk)
        self.fields['location'] = forms.ModelChoiceField(initial=location, queryset=Place.objects.all())
        self.fields['category'] = forms.ChoiceField(choices=CasePlace.CAT_CHOICES, initial=CasePlace.VISIT)
        self.fields['date_from'] = forms.DateField(initial=datetime.date.today(), input_formats=['%Y-%m-%d'])
        self.fields['date_to'] = forms.DateField(initial=datetime.date.today(), input_formats=['%Y-%m-%d'])
