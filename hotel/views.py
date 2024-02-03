from django.shortcuts import render,redirect
from django.db.models import Q,Prefetch
from django.forms import modelform_factory
from .forms import *
from django.contrib import messages
import requests
from django.core import serializers
# Create your views here.
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
import environ
import os
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

def formatear_respuesta(response):
    # Implementa la lógica para formatear la respuesta según su tipo
    content_type = response.headers.get('content-type', '').lower()

    if 'json' in content_type:
        return response.json()
    elif 'xml' in content_type:
        # Implementa la lógica para parsear XML
        pass
    elif 'html' in content_type:
        # Implementa la lógica para manejar HTML
        pass
    else:
        # Manejar otros tipos de contenido según sea necesario
        pass


def index(request):
    return render(request,'index.html')

def crear_cabecera():
    #return {'Authorization': f'Bearer {env("NEW_TOKEN")}'}
    return {'Authorization': f'Bearer {env("BEARER")}'}


def usuarios_lista_api(request):
    headers = crear_cabecera()
    # En caso de que tengamos un dominio o una version diferente, la modificamos directamente en el .env y será modificado en todas views   
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/usuarios', headers=headers)
    usuarios = formatear_respuesta(response)
    return render(request, 'usuario/lista_api.html', {"usuarios_mostrar": usuarios})

def clientes_lista_api(request):
    headers =  crear_cabecera()
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/clientes', headers=headers)
    clientes = formatear_respuesta(response)
    return render(request, 'cliente/lista_api.html',{"clientes_mostrar":clientes})

def clientes_lista_api_mejorada(request):
    headers = crear_cabecera()
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/clientes/mejorado', headers=headers)
    clientes = formatear_respuesta(response)
    return render(request, 'cliente/lista_api_mejorada.html', {"clientes_mostrar": clientes})


def habitaciones_lista_api(request):
    headers = crear_cabecera()
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/habitaciones', headers=headers)
    habitaciones = formatear_respuesta(response)
    return render(request, 'habitacion/habitacion_list.html', {"habitaciones_mostrar": habitaciones})

def habitaciones_lista_api_mejorada(request):
    headers = crear_cabecera()
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/habitaciones/mejorado', headers=headers)
    habitaciones = formatear_respuesta(response)
    return render(request, 'habitacion/habitacion_list_mejorada.html', {"habitaciones_mostrar": habitaciones})

def reservas_lista_api(request):
    headers =  crear_cabecera()
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/reservas',headers=headers)
    reservas = formatear_respuesta(response)
    return render(request,'reserva/reserva_list.html',{"reservas_mostrar":reservas})

def reservas_lista_api_mejorada(request):
    headers = crear_cabecera()
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/reservas/mejorado', headers=headers)
    reservas = formatear_respuesta(response)
    return render(request, 'reserva/reserva_list_mejorada.html', {"reservas_mostrar": reservas})


def cliente_busqueda_simple(request):
    formulario = BusquedaClienteForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get(
            f'{env("DOMINIO")}{env("VERSION")}/cliente_buscar',
            headers = headers,
            params = formulario.cleaned_data
        )
        clientes = formatear_respuesta(response)
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
                f'{env("DOMINIO")}{env("VERSION")}/cliente_busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                clientes = formatear_respuesta(response)
                return render(request, 'cliente/lista_api.html',
                                {"clientes_mostrar":clientes})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = formatear_respuesta(response)
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

def habitacion_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaHabitacionForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                f'{env("DOMINIO")}{env("VERSION")}/habitacion_busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                habitaciones = formatear_respuesta(response)
                return render(request, 'habitacion/lista_api.html',
                                {"habitaciones_mostrar":habitaciones})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = formatear_respuesta(response)
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'habitacion/habitacion_busqueda.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaHabitacionForm(None)
    return render(request, 'habitacion/habitacion_busqueda.html',{"formulario":formulario})

def reserva_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaReservaForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                f'{env("DOMINIO")}{env("VERSION")}/reserva_busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                reservas = formatear_respuesta(response)
                return render(request, 'reserva/lista_api.html',
                                {"reservas_mostrar":reservas})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = formatear_respuesta(response)
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'reserva/reserva_busqueda.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaReservaForm(None)
    return render(request, 'reserva/reserva_busqueda.html',{"formulario":formulario})


#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)