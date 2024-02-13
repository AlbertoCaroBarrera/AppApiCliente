from requests.exceptions import HTTPError
from django.shortcuts import render,redirect
from django.db.models import Q,Prefetch
from django.forms import modelform_factory
from .forms import *
from django.contrib import messages
import requests
from django.core import serializers
import json
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

# Autenticacion dependiendo de si es OUATH 2 o JWT
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
    return render(request, 'habitacion/lista_api.html', {"habitaciones_lista_api": habitaciones})

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




#CREATE RESERVAS
def reservas_crear(request):
    if (request.method == "POST"):
        try:
            formulario = ReservaForm(request.POST)
            headers =  {
                        'Authorization': 'Bearer '+env("BEARER"),
                        "Content-Type": "application/json"  
                    } 
            datos = formulario.data.copy()
            datos["cliente"] = request.POST.get("cliente");
            datos["habitacion"] = request.POST.get("habitacion")
            datos["fecha_entrada"] = str(datetime.strptime(datos['fecha_entrada'], '%Y-%m-%dT%H:%M'))
            datos["fecha_salida"] = str(datetime.strptime(datos['fecha_salida'], '%Y-%m-%dT%H:%M'))
            response = requests.post(
                f'{env("DOMINIO")}{env("VERSION")}/reservas/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha creado la reserva correctamente.')
                return redirect("reservas_lista_api")
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
                            'reserva/create.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    else:
        formulario = ReservaForm(None)
    return render(request, 'reserva/create.html',{"formulario":formulario})


def reserva_editar(request,reserva_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    reserva = helper.obtener_reserva(reserva_id)

    fecha_hora_str = reserva['fecha_entrada']
    fecha_hora_str_sin_dos_puntos = fecha_hora_str[:-3] + fecha_hora_str[-2:]
    
    formulario = ReservaForm(datosFormulario,
            initial={
                'cliente': reserva['cliente'],
                'habitacion': reserva["habitacion"],
                'fecha_entrada': datetime.strptime(fecha_hora_str_sin_dos_puntos, '%Y-%m-%dT%H:%M:%S%z'),
            
            }
    )
    if (request.method == "POST"):
        try:
            formulario = ReservaForm(request.POST)
            headers =  {
                        'Authorization': 'Bearer '+env("BEARER"),
                        "Content-Type": "application/json"  
                    } 
            datos = request.POST.copy()
            datos["cliente"] = request.POST.get("cliente");
            datos["habitacion"] = request.POST.get("habitacion")
            datos["fecha_entrada"] = str(datetime.strptime(datos['fecha_entrada'], '%Y-%m-%dT%H:%M:%S%z'))
            datos["fecha_salida"] = str(datetime.strptime(datos['fecha_salida'], '%Y-%m-%dT%H:%M:%S%z'))
            
            response = requests.put(
                'http://127.0.0.1:8080/api/v1/reserva/editar/'+str(reserva_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha editado la reserva correctamente.')
                
                return redirect("reserva_mostrar",reserva_id=reserva_id)
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
                            'reserva/actualizar.html',
                            {"formulario":formulario,"reserva":reserva})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'reserva/actualizar.html',{"formulario":formulario,"reserva":reserva})

def reserva_editar_fecha(request,reserva_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    reserva = helper.obtener_reserva(reserva_id)
    formulario = ReservaActualizarFechaForm(datosFormulario,
            initial={
                'fecha_entrada': reserva['fecha_entrada'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = ReservaForm(request.POST)
            headers =  {
                        'Authorization': 'Bearer '+env("BEARER"),
                        "Content-Type": "application/json"  
                    } 
            datos = request.POST.copy()
            response = requests.patch(
                'http://127.0.0.1:8080/api/v1/reserva/actualizar/fecha/'+str(reserva_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha editado la reserva correctamente.')
                
                return redirect("reserva_mostrar")
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
                            'reserva/actualizar_fecha_reserva.html',
                            {"formulario":formulario,"reserva":reserva})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'reserva/actualizar_fecha_reserva.html',{"formulario":formulario,"reserva":reserva})


def reserva_eliminar(request,reserva_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
            'http://127.0.0.1:8080/api/v1/reserva/eliminar/'+str(reserva_id),
            headers=headers,
        )
        if(response.status_code == requests.codes.ok):
            messages.success(request, 'Se ha eliminado la reserva correctamente.')
            
            return redirect("reservas_lista_api")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('reservas_lista_api')

# CLIENTES
def clientes_crear(request):
    if (request.method == "POST"):
        try:
            formulario = ClienteForm(request.POST)
            headers =  {
                        'Authorization': 'Bearer '+env("BEARER"),
                        "Content-Type": "application/json" 
                    } 
            datos = formulario.data.copy()
            datos["nombre"] = request.POST.get("nombre");
            datos["correo_electronico"] = request.POST.get("correo_electronico")
            datos["telefono"] = request.POST.get("telefono")
            datos["direccion"] = request.POST.get("direccion")
            
            response = requests.post(
                f'{env("DOMINIO")}{env("VERSION")}/clientes/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha creado al cliente correctamente.')
                
                return redirect("clientes_lista_api")
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
                            'cliente/create.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    else:
        formulario = ClienteForm(None)
    return render(request, 'cliente/create.html',{"formulario":formulario})


def cliente_editar(request,cliente_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    cliente = helper.obtener_cliente(cliente_id)
    formulario = ClienteForm(datosFormulario,
            initial={
                'nombre': cliente['nombre'],
                'correo_electronico': cliente["correo_electronico"],
                'telefono': cliente["telefono"],
                'direccion': cliente["direccion"],

            }
    )
    if (request.method == "POST"):
        try:
            formulario = ClienteForm(request.POST)
            headers =  {
                        'Authorization': 'Bearer '+env("BEARER"),
                        "Content-Type": "application/json"  
                    } 
            datos = request.POST.copy()
            datos["nombre"] = request.POST.get("nombre");
            datos["correo_electronico"] = request.POST.get("correo_electronico")
            datos["telefono"] = request.POST.get("telefono")
            datos["direccion"] = request.POST.get("direccion")

           
            response = requests.put(
                'http://127.0.0.1:8080/api/v1/cliente/editar/'+str(cliente_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha editado la cliente correctamente.')
                
                return redirect("clientes_lista_api")
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
                            'cliente/actualizar.html',
                            {"formulario":formulario,"cliente":cliente})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'cliente/actualizar.html',{"formulario":formulario,"cliente":cliente})

def cliente_editar_nombre(request,cliente_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    cliente = helper.obtener_cliente(cliente_id)
    formulario = ClienteActualizarNombreForm(datosFormulario,
            initial={
                'nombre': cliente['nombre'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = ClienteForm(request.POST)
            headers = headers =  {
                        'Authorization': 'Bearer '+env("BEARER"),
                        "Content-Type": "application/json"  
                    } 
            datos = request.POST.copy()
            response = requests.patch(
                'http://127.0.0.1:8080/api/v1/cliente/actualizar/nombre/'+str(cliente_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha editado la cliente correctamente.')
                
                return redirect("clientes_lista_api")
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
                            'cliente/actualizar_nombre_cliente.html',
                            {"formulario":formulario,"cliente":cliente})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'cliente/actualizar_nombre_cliente.html',{"formulario":formulario,"cliente":cliente})

def cliente_eliminar(request,cliente_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
            'http://127.0.0.1:8080/api/v1/cliente/eliminar/'+str(cliente_id),
            headers=headers,
        )
        if(response.status_code == requests.codes.ok):
            messages.success(request, 'Se ha eliminado la cliente correctamente.')
            
            return redirect("clientes_lista_api")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('clientes_lista_api')


# Habitacion

def Habitacion_crear(request):
    if (request.method == "POST"):
        try:
            formulario = HabitacionForm(request.POST)
            headers =  {
                        'Authorization': 'Bearer '+env("BEARER"),
                        "Content-Type": "application/json" 
                    } 
            datos = formulario.data.copy()
            datos["numero_hab"] = request.POST.get("numero_hab");
            datos["tipo"] = request.POST.get("tipo")
            datos["precio_noche"] = request.POST.get("precio_noche")
            
            response = requests.post(
                f'{env("DOMINIO")}{env("VERSION")}/habitacion/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha creado la habitacion correctamente.')
                
                return redirect("habitaciones_lista_api")
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
                            'habitacion/create.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    else:
        formulario = HabitacionForm(None)
    return render(request, 'habitacion/create.html',{"formulario":formulario})

def habitacion_editar(request,habitacion_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    habitacion = helper.obtener_habitacion(habitacion_id)
    formulario = HabitacionForm(datosFormulario,
            initial={
                'numero_hab': habitacion['numero_hab'],
                'tipo': habitacion['tipo'],
                'precio_noche': habitacion['precio_noche']
            }
    )
    if (request.method == "POST"):
        try:
            formulario = HabitacionForm(request.POST)
            headers =  {
                        'Authorization': 'Bearer '+env("BEARER"),
                        "Content-Type": "application/json"  
                    } 
            datos = request.POST.copy()
            datos["numero_hab"] = int(request.POST.get("numero_hab"));
            datos["tipo"] = request.POST.get("tipo")
            datos["precio_noche"] = float(request.POST.get("precio_noche"))
            response = requests.put(
                'http://127.0.0.1:8080/api/v1/habitacion/editar/'+str(habitacion_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha editado la habitacion correctamente.')
                
                return redirect("habitaciones_lista_api")
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
                            'habitacion/actualizar.html',
                            {"formulario":formulario,"habitacion":habitacion})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'habitacion/actualizar.html',{"formulario":formulario,"habitacion":habitacion})


def habitacion_editar_nombre(request,habitacion_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    habitacion = helper.obtener_habitacion(habitacion_id)
    formulario = HabitacionActualizarNombreForm(datosFormulario,
            initial={
                'tipo': habitacion['tipo'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = HabitacionForm(request.POST)
            headers =  {
                        'Authorization': 'Bearer '+env("BEARER"),
                        "Content-Type": "application/json"  
                    } 
            datos = request.POST.copy()
            response = requests.patch(
                'http://127.0.0.1:8080/api/v1/habitacion/actualizar/nombre/'+str(habitacion_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha editado la habitacion correctamente.')
                
                return redirect("habitaciones_lista_api")
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
                            'habitacion/actualizar_nombre_habitacion.html',
                            {"formulario":formulario,"habitacion":habitacion})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'habitacion/actualizar_nombre_habitacion.html',{"formulario":formulario,"habitacion":habitacion})

def habitacion_eliminar(request,habitacion_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
            'http://127.0.0.1:8080/api/v1/habitacion/eliminar/'+str(habitacion_id),
            headers=headers,
        )
        if(response.status_code == requests.codes.ok):
            messages.success(request, 'Se ha eliminado la habitacion correctamente.')
            return redirect("habitaciones_lista_api")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('habitaciones_lista_api')

#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)

