from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date, datetime
from django.contrib.auth.forms import UserCreationForm
from .helper import helper
from django.contrib.auth.models import User
class BusquedaClienteForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
    
class BusquedaAvanzadaClienteForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    telefono = forms.IntegerField(required=False)

class BusquedaAvanzadaHabitacionForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    
    numero_hab  = forms.IntegerField(required=False)
    
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
        
        self.request = kwargs.pop("request_usuario")
        super(ReservaForm,self).__init__(*args, **kwargs)
        
        clientesDisponibles = helper.obtener_clientes_select(self.request )
        
        self.fields['cliente'] = forms.ChoiceField(choices=clientesDisponibles,
                                                    widget=forms.Select,
                                                    required=True)
        
        habitacionesDisponibles = helper.obtener_habitaciones_select(self.request )
        self.fields['habitacion'] = forms.ChoiceField(choices=habitacionesDisponibles,
                                                    widget=forms.Select,
                                                    required=True)
    def clean(self):
        cleaned_data = super().clean()
        fecha_entrada = cleaned_data.get("fecha_entrada")
        fecha_salida = cleaned_data.get("fecha_salida")

        if fecha_entrada and fecha_salida:
            if fecha_entrada >= fecha_salida:
                raise forms.ValidationError("La fecha de salida debe ser posterior a la fecha de entrada.")

            if fecha_entrada < datetime.now():
                raise forms.ValidationError("La fecha de entrada no puede ser en el pasado.")

        return cleaned_data
class ReservaActualizarFechaForm(forms.Form):
    fecha_entrada = forms.DateTimeField(label="Fecha y Hora Hasta",
                                       required=True,
                                       widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
        
        
class ClienteForm(forms.Form):
    nombre = forms.CharField(label="Nombre",
                             required=True,
                             max_length=200,
                             help_text="200 caracteres maximo")
    
    correo_electronico = forms.EmailField(label="Correo Electrónico",max_length=200,required=True)
    
    telefono = forms.CharField(label="Teléfono",required=True,max_length=200)
    
    direccion = forms.CharField(widget=forms.Textarea)

class ClienteActualizarNombreForm(forms.Form):
    nombre = forms.CharField(label="nombre de la cliente",
                             required=True, 
                             max_length=200,
                             help_text="200 caracteres como máximo")


class HabitacionForm(forms.Form):
    numero_hab = forms.IntegerField(label="Número de Habitación",required=True)
    
    tipo = forms.CharField(max_length=200,required=True)
    
    precio_noche = forms.FloatField(required=True)
    
class HabitacionActualizarNombreForm(forms.Form):
    tipo = forms.CharField(label="tipo de la habitacion",
                            required=True, 
                            max_length=200,
                            help_text="200 caracteres como máximo")

class RegistroForm(UserCreationForm):
    roles = (
        (2,'cliente'),
        (3, 'empleado'),
    )
    
    rol = forms.ChoiceField(choices=roles)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'rol')
        

class LoginForm(forms.Form):
    usuario = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    
class FavoritoForm(forms.Form):
    habitacion = forms.CharField(label="numero"
                                  ,required=False)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request_usuario")
        
        super(FavoritoForm, self).__init__(*args, **kwargs)
        
        habitacionesDisponibles = helper.obtener_habitaciones_select(self.request)
        self.fields["habitacion"] = forms.ChoiceField(
            choices= habitacionesDisponibles,
            required=True,
            help_text="Mantén pulsada la tecla control para seleccionar un plato"
        )   