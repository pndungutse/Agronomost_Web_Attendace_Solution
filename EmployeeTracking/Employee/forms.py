from django.contrib.auth import models
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from .models import Agronomist, Attendence_Agr, Staff, Location, Agronomist_location, Attendence_Agr

class Agronomist_locationForm(forms.ModelForm):
    class Meta:
        model = Agronomist_location
        fields = '__all__'
        labels = {
            'agronomist':'Agronomist',
            'location':'Location'
        }
    
class LocationForm(forms.ModelForm):
    latitude = forms.FloatField(initial=0.0)
    longitude = forms.FloatField(initial=0.0)
    class Meta:
        model = Location
        fields = '__all__'
        labels = {
            'place_name':'Place Name',
            'latitude':'Latitude',
            'longitude':'Longitude'
        }
        
class Attendence_AgrForm(forms.ModelForm):
    class Meta:
        model = Attendence_Agr
        fields = ('attendance_type',)
        labels = {
            'attendance_type':'Attendance Type',
        }
        
class AgronomistForm(forms.ModelForm):
    
    class Meta:
        model = Agronomist
        fields = ('agr_code', 'first_name', 'last_name','phone','email', 'user')
        labels = {
            'agr_code' : 'Agronomist Code',
            'first_name' : 'First Name',
            'last_name' : 'Last Name',
            'phone' : 'Phone',
            'email' : 'Email',
            'user' : 'user'
        }
        