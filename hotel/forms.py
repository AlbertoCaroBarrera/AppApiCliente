from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime
from django.contrib.auth.forms import UserCreationForm
from .helper import helper
class BusquedaClienteForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
    
class BusquedaAvanzadaClienteForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    telefono = forms.IntegerField(required=False)

class BusquedaAvanzadaHabitacionForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    
    cd  = forms.IntegerField(required=False)
    
    precio_noche = forms.FloatField(required=False)

class BusquedaAvanzadaReservaForm(forms.Form):

    textoBusqueda = forms.CharField(required=False)
    fecha_desde = forms.DateField(required=False, label='Fecha de entrada desde')
    fecha_hasta = forms.DateField(required=False, label='Fecha de entrada hasta')


class ReservaForm(forms.Form):
    fecha_entrada = forms.DateTimeField(label="Fecha de entrada")

    fecha_salida = forms.DateTimeField(label="Fecha de salida")

    def __init__(self,*args, **kwargs):
        super(ReservaForm,self).__init__(*args, **kwargs)
        
        clientesDisponibles = helper.obtener_clientes_select()
        self.fields['cliente'] = forms.ChoiceField(choices=clientesDisponibles,
                                                    widget=forms.Select,
                                                    required=True)
        
        habitacionesDisponibles = helper.obtener_habitaciones_disponibles()
        self.fields['habitacion'] = forms.ChoiceField(choices=habitacionesDisponibles,
                                                    widget=forms.Select,
                                                    required=True)
        
        