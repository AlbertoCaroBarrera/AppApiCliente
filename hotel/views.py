from requests.exceptions import HTTPError
from django.shortcuts import render,redirect
from django.db.models import Q,Prefetch
from django.forms import modelform_factory
from .forms import *
from django.contrib import messages
import requests
from django.core import serializers
import json
from django.contrib.auth.decorators import permission_required
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
    imagenes = helper.imagenes()["mediana"]
    return render(request,'index.html',{'imagenes':imagenes})

# Autenticacion dependiendo de si es OUATH 2 o JWT
def crear_cabecera():
    #return {'Authorization': f'Bearer {env("NEW_TOKEN")}'}
    return {'Authorization': f'Bearer {env("BEARER")}'}

def crear_cabecera_cliente(request):
    return {
                        'Authorization': 'Bearer '+ request.session["token"],
                        "Content-Type": "application/json" 
                    } 

def usuarios_lista_api(request):
    headers = crear_cabecera_cliente(request)
    # En caso de que tengamos un dominio o una version diferente, la modificamos directamente en el .env y será modificado en todas views   
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/usuarios', headers=headers)
    usuarios = formatear_respuesta(response)
    return render(request, 'usuario/lista_api.html', {"usuarios_mostrar": usuarios})

def clientes_lista_api(request):
    headers =  crear_cabecera_cliente(request)
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/clientes', headers=headers)
    clientes = formatear_respuesta(response)
    return render(request, 'cliente/lista_api.html',{"clientes_mostrar":clientes})

def eventos_mes_api(request):
    headers =  crear_cabecera_cliente(request)
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/eventos/mes', headers=headers)
    eventos = formatear_respuesta(response)
    return render(request, 'evento/mensual.html',{"eventosMes":eventos})


def clientes_lista_api_mejorada(request):
    headers = crear_cabecera_cliente(request)
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/clientes/mejorado', headers=headers)
    clientes = formatear_respuesta(response)
    return render(request, 'cliente/lista_api_mejorada.html', {"clientes_mostrar": clientes})

def habitaciones_lista_api(request):
    imagenes = helper.imagenes()
    tipo_habitacion = request.GET.get('tipo_habitacion', 'pequeña')
    if tipo_habitacion == 'pequeña':
        imagenes = imagenes["pequeña"]
    elif tipo_habitacion == 'mediana':
        imagenes = imagenes["mediana"]
    elif tipo_habitacion == 'grande':
        imagenes = imagenes["grande"]
    elif tipo_habitacion == 'deluxe':
        imagenes = imagenes["deluxe"]
    else:
        imagenes = imagenes["pequeña"]
    orden="precio"
    if request.GET.get('orden') is not None:
        orden = request.GET.get('orden')
    aniversario = helper.es_aniversario(request.session["usuario"]["date_joined"])
    descuento = 1
    rebaja=False
    if aniversario:
        descuento = 0.90
        rebaja = True
    headers = crear_cabecera_cliente(request)
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/habitaciones/{orden}', headers=headers)
    habitaciones = formatear_respuesta(response)

    # Calcula el precio con descuento para cada habitación
    for habitacion in habitaciones:
        habitacion['precio_con_descuento'] = habitacion['precio_noche'] * descuento
        
    
    
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/servicios', headers=headers)
    servicios = formatear_respuesta(response)
    
    formulario = ReservaForm(None, request_usuario=request)
    return render(request, 'habitacion/lista_api.html', {"habitaciones_lista_api": habitaciones, "descuento": descuento, "servicios":servicios,"rebaja":rebaja,"formulario":formulario,"imagenes":imagenes})
    


def detalle_habitacion(request, habitacion_id):
    hab = ""
    servicio = request.POST.get('servicio', None)
    servicio_str = servicio.replace(',', '.')
    servicio = float(servicio_str)
    headers = crear_cabecera_cliente(request)
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/habitaciones', headers=headers)
    habitaciones = formatear_respuesta(response)

    for habitacion in habitaciones:
        if habitacion['id'] == habitacion_id:
            hab = habitacion
            break
    aniversario = helper.es_aniversario(request.session["usuario"]["date_joined"])
    descuento = 1
    if aniversario:
        descuento = 0.90
        precio_final = hab["precio_noche"]* descuento + servicio
        
    else:
        precio_final = hab.precio_noche + servicio
        
    context = {
        'habitacion': hab,
        'servicio': servicio,
        'precio_final': round(precio_final,2)
    }
    
    if (request.method == "POST"):
        try:
            formulario = ReservaForm(request.POST, request_usuario=request)
            headers =  crear_cabecera_cliente(request) 
            datos = formulario.data.copy()
            datos["fecha_entrada"] = str(datetime.strptime(datos['fecha_entrada'], '%Y-%m-%dT%H:%M'))
            datos["fecha_salida"] = str(datetime.strptime(datos['fecha_salida'], '%Y-%m-%dT%H:%M'))
            cliente_id = helper.obtener_id_cliente(str(request.session["usuario"]["id"]),request)
            nuevos_datos = {
                            "csrfmiddlewaretoken": datos["csrfmiddlewaretoken"],
                            "cliente": cliente_id,
                            "habitacion":habitacion_id,
                            **{key: datos[key] for key in datos if key != "csrfmiddlewaretoken"}
}
            del nuevos_datos["servicio"]
            response = requests.post(
                f'{env("DOMINIO")}{env("VERSION")}/reservas/crear',
                headers=headers,
                data=json.dumps(nuevos_datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha creado la reserva correctamente.')
                return render(request, 'habitacion/detalle_habitacion.html',{"habitacion":hab,"precio_final":precio_final})
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
                            'habitacion/lista_api.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
            
    else:
        formulario = ReservaForm(None, request_usuario=request)
    return render(request, 'habitacion/lista_api.html', context)


def habitaciones_lista_api_mejorada(request):
    headers = crear_cabecera_cliente(request)
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/habitaciones/mejorado', headers=headers)
    habitaciones = formatear_respuesta(response)
    return render(request, 'habitacion/habitacion_list_mejorada.html', {"habitaciones_mostrar": habitaciones})

def reservas_lista_api(request):
    headers =  crear_cabecera_cliente(request)
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/reservas',headers=headers)
    reservas = formatear_respuesta(response)
    nombre = helper.obtener_nombre(request.session["usuario"]["id"],request)
    reservas= [reserva for reserva in reservas if helper.obtener_nombre(reserva["cliente"],request) == nombre]
    return render(request,'reserva/reserva_list.html',{"reservas_mostrar":reservas,"nombre":nombre})

def reservas_lista_api_mejorada(request):
    headers = crear_cabecera_cliente(request)
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/reservas/mejorado', headers=headers)
    reservas = formatear_respuesta(response)
    return render(request, 'reserva/reserva_list_mejorada.html', {"reservas_mostrar": reservas})


def cliente_busqueda_simple(request):
    formulario = BusquedaClienteForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera_cliente(request)
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
            headers = crear_cabecera_cliente(request)
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
            headers = crear_cabecera_cliente(request)
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
            headers = crear_cabecera_cliente(request)
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
            formulario = ReservaForm(request.POST, request_usuario=request)
            headers =  crear_cabecera_cliente(request) 
            datos = formulario.data.copy()
            datos["habitacion"] = request.POST.get("habitacion")
            datos["fecha_entrada"] = str(datetime.strptime(datos['fecha_entrada'], '%Y-%m-%dT%H:%M'))
            datos["fecha_salida"] = str(datetime.strptime(datos['fecha_salida'], '%Y-%m-%dT%H:%M'))
            cliente_id = helper.obtener_id_cliente(str(request.session["usuario"]["id"]),request)
            nuevos_datos = {
                            "csrfmiddlewaretoken": datos["csrfmiddlewaretoken"],
                            "cliente": cliente_id,
                            **{key: datos[key] for key in datos if key != "csrfmiddlewaretoken"}
}
            response = requests.post(
                f'{env("DOMINIO")}{env("VERSION")}/reservas/crear',
                headers=headers,
                data=json.dumps(nuevos_datos)
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
        formulario = ReservaForm(None, request_usuario=request)
    return render(request, 'reserva/create.html',{"formulario":formulario})


def reserva_editar(request,reserva_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    reserva = helper.obtener_reserva(reserva_id,request)

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
            formulario = ReservaForm(request.POST, request_usuario=request)
            headers =  crear_cabecera_cliente(request) 
            datos = request.POST.copy()
            datos["cliente"] = request.POST.get("cliente");
            datos["habitacion"] = request.POST.get("habitacion")
            datos["fecha_entrada"] = str(datetime.strptime(datos['fecha_entrada'], '%Y-%m-%dT%H:%M:%S%z'))
            datos["fecha_salida"] = str(datetime.strptime(datos['fecha_salida'], '%Y-%m-%dT%H:%M:%S%z'))
            
            response = requests.put(
                'https://AlbertoCaroBarrera.pythonanywhere.com/api/v1/reserva/editar/'+str(reserva_id),
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
    
    reserva = helper.obtener_reserva(reserva_id,request)
    formulario = ReservaActualizarFechaForm(datosFormulario,
            initial={
                'fecha_entrada': reserva['fecha_entrada'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = ReservaForm(request.POST, request_usuario=request)
            headers =  crear_cabecera_cliente(request) 
            datos = request.POST.copy()
            response = requests.patch(
                'https://AlbertoCaroBarrera.pythonanywhere.com/api/v1/reserva/actualizar/fecha/'+str(reserva_id),
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
        headers = crear_cabecera_cliente(request)
        response = requests.delete(
            'https://AlbertoCaroBarrera.pythonanywhere.com/api/v1/reserva/eliminar/'+str(reserva_id),
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
            headers =  crear_cabecera_cliente(request)
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
    
    cliente = helper.obtener_cliente(cliente_id,request)
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
            headers =  crear_cabecera_cliente(request) 
            datos = request.POST.copy()
            datos["nombre"] = request.POST.get("nombre");
            datos["correo_electronico"] = request.POST.get("correo_electronico")
            datos["telefono"] = request.POST.get("telefono")
            datos["direccion"] = request.POST.get("direccion")

           
            response = requests.put(
                'https://AlbertoCaroBarrera.pythonanywhere.com/api/v1/cliente/editar/'+str(cliente_id),
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
    
    cliente = helper.obtener_cliente(cliente_id,request)
    formulario = ClienteActualizarNombreForm(datosFormulario,
            initial={
                'nombre': cliente['nombre'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = ClienteForm(request.POST)
            headers = crear_cabecera_cliente(request)
            datos = request.POST.copy()
            response = requests.patch(
                'https://AlbertoCaroBarrera.pythonanywhere.com/api/v1/cliente/actualizar/nombre/'+str(cliente_id),
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
        headers = crear_cabecera_cliente(request)
        response = requests.delete(
            'https://AlbertoCaroBarrera.pythonanywhere.com/api/v1/cliente/eliminar/'+str(cliente_id),
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
                        'Authorization': 'Bearer '+ request.session["token"],
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
    
    habitacion = helper.obtener_habitacion(habitacion_id,request)
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
            datos = request.POST.copy()
            datos["numero_hab"] = int(request.POST.get("numero_hab"));
            datos["tipo"] = request.POST.get("tipo")
            datos["precio_noche"] = float(request.POST.get("precio_noche"))
            response = requests.put(
                'https://AlbertoCaroBarrera.pythonanywhere.com/api/v1/habitacion/editar/'+str(habitacion_id),
                headers=crear_cabecera_cliente(request)
,
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
    
    habitacion = helper.obtener_habitacion(habitacion_id,request)
    formulario = HabitacionActualizarNombreForm(datosFormulario,
            initial={
                'tipo': habitacion['tipo'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = HabitacionForm(request.POST)
            datos = request.POST.copy()
            response = requests.patch(
                'https://AlbertoCaroBarrera.pythonanywhere.com/api/v1/habitacion/actualizar/nombre/'+str(habitacion_id),
                headers=crear_cabecera_cliente(request),
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
        headers = crear_cabecera_cliente(request)
        response = requests.delete(
            'https://AlbertoCaroBarrera.pythonanywhere.com/api/v1/habitacion/eliminar/'+str(habitacion_id),
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

# Registro

def registrar_usuario(request):
    if (request.method == "POST"):
        try:
            formulario = RegistroForm(request.POST)
            if(formulario.is_valid()):
                headers =  {
                            "Content-Type": "application/json" 
                        }
                response = requests.post(
                    'https://AlbertoCaroBarrera.pythonanywhere.com/api/v1/registrar/usuario',
                    headers=headers,
                    data=json.dumps(formulario.cleaned_data)
                )
                
                if(response.status_code == requests.codes.ok):
                    usuario = response.json()
                    token_acceso = helper.obtener_token_session(
                            formulario.cleaned_data.get("username"),
                            formulario.cleaned_data.get("password1")
                            )
                    request.session["usuario"]=usuario
                    request.session["token"] = token_acceso
                    return redirect("index")
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
                            'registration/signup.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
            
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})

def login(request):
    if (request.method == "POST"):
        formulario = LoginForm(request.POST)
        try:
            token_acceso = helper.obtener_token_session(
                                formulario.data.get("usuario"),
                                formulario.data.get("password")
                                )
            request.session["token"] = token_acceso


            headers = {'Authorization': 'Bearer '+token_acceso} 
            response = requests.get('https://AlbertoCaroBarrera.pythonanywhere.com/api/v1/usuario/token/'+token_acceso,headers=headers)
            usuario = response.json()
            request.session["usuario"] = usuario
            
            return  redirect("index")
        except Exception as excepcion:
            print(f'Hubo un error en la petición: {excepcion}')
            formulario.add_error("usuario",excepcion)
            formulario.add_error("password",excepcion)
            return render(request, 
                            'registration/login.html',
                            {"form":formulario})
    else:  
        formulario = LoginForm()
    return render(request, 'registration/login.html', {'form': formulario})



def logout(request):
    del request.session['token']
    return redirect('index')


# favoritos

def favoritos_lista_api(request):

    headers = crear_cabecera_cliente(request)
    cliente_id=request.session["usuario"]["id"] #para obtener el id del usuario logueado
    response = requests.get('https://AlbertoCaroBarrera.pythonanywhere.com/api/v1/' + 'favoritos/usuario/'+str(cliente_id), headers=headers)
    response.raise_for_status()  # Lanza una excepción si hay un error HTTP
    
    favoritos = formatear_respuesta(response) #llamamos a la función para que procese que tipo de dato es
    
    if favoritos is not None:
        return render(request, 'habitacion/habitaciones_favoritas.html', {'favoritos_mostrar': favoritos})
    else:
        return render(request, 'errores/500.html',None,None,500)

def favorito_crear(request):
    cliente_id = request.session["usuario"]["id"] #para obtener el id del usuario logueado
    if (request.method == "POST"):
        try:
            formulario = FavoritoForm(request.POST,request_usuario=request)
            headers =  crear_cabecera_cliente(request) 
            datos = formulario.data.copy()
            datos["cliente"] = cliente_id
            response = requests.post(
                'https://AlbertoCaroBarrera.pythonanywhere.com/api/v1/'+ 'favoritos/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha agregado correctamente la habitacion.')
                return redirect("favoritos_lista")
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
                            'habitacion/crearFavorita.html',
                            {"formulario":formulario})
            else:
                return render(request, 'errores/500.html',None,None,500)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return render(request, 'errores/500.html',None,None,500)
        
    else:
         formulario = FavoritoForm(None,request_usuario=request)
    return render(request, 'habitacion/crearFavorita.html',{"formulario":formulario})

def servicios_list(request):
    headers = crear_cabecera_cliente(request)
    response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/servicios', headers=headers)
    servicios = formatear_respuesta(response)
    return render(request, 'servicio/servicioconreserva.html', {"servicios_mostrar": servicios})


    