from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime
from django.contrib.auth.forms import UserCreationForm

class BusquedaClienteForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
    
class BusquedaAvanzadaClienteForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    telefono = forms.IntegerField(required=False)