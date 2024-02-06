from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date, datetime
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
    fecha_entrada = forms.DateField(label="Fecha Desde",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(1990,2030))
                                )

    fecha_salida = forms.DateField(label="Fecha Hasta",
                                  required=False,
                                  widget= forms.SelectDateWidget(years=range(1990,2030))

)

    def __init__(self,*args, **kwargs):
        super(ReservaForm,self).__init__(*args, **kwargs)
        
        clientesDisponibles = helper.obtener_clientes_select()
        self.fields['cliente'] = forms.ChoiceField(choices=clientesDisponibles,
                                                    widget=forms.Select,
                                                    required=True)
        
        habitacionesDisponibles = helper.obtener_habitaciones_select()
        self.fields['habitacion'] = forms.ChoiceField(choices=habitacionesDisponibles,
                                                    widget=forms.Select,
                                                    required=True)
        
        