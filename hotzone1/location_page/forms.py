from django import forms
from hotzoneData.models import Place
from django.forms import widgets

class locationEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        super(locationEditForm, self).__init__(*args, **kwargs)
        location = Place.objects.get(pk=pk)
        self.fields['location'] = forms.CharField(max_length=100, initial=location.location)
        self.fields['address'] = forms.CharField(max_length=100, initial=location.address)
        self.fields['x'] = forms.IntegerField(initial=location.x_coor)
        self.fields['y'] = forms.IntegerField(initial=location.y_coor)
