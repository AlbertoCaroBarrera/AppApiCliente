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
    fecha_actual = datetime.now().strftime('%Y-%m-%dT%H:%M')  # Obtiene la fecha y hora actuales en formato datetime-local
    
    fecha_entrada = forms.DateTimeField(label="Fecha y Hora Desde",
                                         required=False,
                                         initial=fecha_actual,  # Establece la fecha y hora actuales como valor predeterminado
                                         widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
                                         )
    
    fecha_salida = forms.DateTimeField(label="Fecha y Hora Hasta",
                                       required=False,
                                       initial=fecha_actual,  # Establece la fecha y hora actuales como valor predeterminado
                                       widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
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
        
        