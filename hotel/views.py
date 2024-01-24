from django.shortcuts import render,redirect
from django.db.models import Q,Prefetch
from django.forms import modelform_factory
from .forms import *
from django.contrib import messages
import requests
from django.core import serializers
# Create your views here.
def index(request):
    return render(request,'index.html')

def crear_cabecera():
    return {'Authorization': 'Bearer 1knFbdNtt7krZd0vEwTWHbAzZoFI9x'}

def clientes_lista_api(request):
    headers =  crear_cabecera()
    response = requests.get('http://127.0.0.1:8000/api/v1/clientes',headers=headers)
    clientes = response.json()
    return render(request, 'cliente/lista_api.html',{"clientes_mostrar":clientes})

def reservas_lista_api(request):
    headers =  crear_cabecera()
    response = requests.get('http://127.0.0.1:8000/api/v1/reservas',headers=headers)
    reservas = response.json()
    return render(request,'reserva/reserva_list.html',{"reservas_mostrar":reservas})


def cliente_busqueda_simple(request):
    formulario = BusquedaClienteForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get(
            'http://127.0.0.1:8000/api/v1/cliente_buscar',
            headers = headers,
            params = formulario.cleaned_data
        )
        clientes = response.json()
        print(clientes)
        return render(request,'cliente/lista_api.html',{"clientes_mostrar":clientes})
    if ('HTTP_REFERER' in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")