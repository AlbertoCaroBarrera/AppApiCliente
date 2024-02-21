
import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()


def crear_cabecera():
    return {'Authorization': f'Bearer {env("BEARER")}'}

def crear_cabecera_cliente(request):
    return {
                        'Authorization': 'Bearer '+ request.session["token"],
                        "Content-Type": "application/json" 
                    } 

class helper:

    def obtener_clientes_select():
        #obtener todos los clientes
        headers = crear_cabecera_cliente(request)
        response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/clientes', headers=headers)
        clientes = response.json()
        lista_clientes = [("","Ninguna")]
        for cliente in clientes:
            lista_clientes.append((cliente['id'], cliente['nombre']))
        return lista_clientes

    def obtener_habitaciones_select():
        #obtener todas las habitaciones
        headers = crear_cabecera_cliente(request)
        response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/habitaciones', headers=headers)
        habitaciones = response.json()

        lista_habitaciones = [("","Ninguna")]
        for habitacion in habitaciones:
            lista_habitaciones.append((habitacion['id'], habitacion['tipo']))
        return lista_habitaciones
    
    def obtener_reserva(id):
        # obtenemos todos las reservas
        headers = crear_cabecera_cliente(request)
        response = requests.get('http://127.0.0.1:8080/api/v1/reserva/'+str(id),headers=headers)
        reserva = response.json()
        return reserva
    
    def obtener_cliente(id):
        # obtenemos todos las clientees
        headers = crear_cabecera_cliente(request)
        response = requests.get('http://127.0.0.1:8080/api/v1/cliente/'+str(id),headers=headers)
        cliente = response.json()
        return cliente

    def obtener_habitacion(id):
        # obtenemos todos las habitaciones
        headers = crear_cabecera_cliente(request)
        response = requests.get('http://127.0.0.1:8080/api/v1/habitacion/'+str(id),headers=headers)
        habitacion = response.json()
        return habitacion
    

    def obtener_token_session(usuario,password):
        token_url = 'http://127.0.0.1:8080/oauth2/token/'
        data = {
            'grant_type': 'password',
            'username': usuario,
            'password': password,
            'client_id': 'admin',
            'client_secret': 'admin',
        }   

        response = requests.post(token_url, data=data)
        respuesta = response.json()
        if response.status_code == 200:
            return respuesta.get('access_token')
        else:
            raise Exception(respuesta.get("error_description"))