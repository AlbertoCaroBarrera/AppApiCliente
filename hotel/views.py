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
    return {'Authorization': 'Bearer QIQOCrVZeSbfHJLK7cGPmM6kDIzmbq'}

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
    
from requests.exceptions import HTTPError
def cliente_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaClienteForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                'http://127.0.0.1:8000/api/v1/cliente_busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                clientes = response.json()
                return render(request, 'cliente/lista_api.html',
                                {"clientes_mostrar":clientes})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'cliente/cliente_busqueda.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaClienteForm(None)
    return render(request, 'cliente/cliente_busqueda.html',{"formulario":formulario})

#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)