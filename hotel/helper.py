
import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

def crear_cabecera():
    return {'Authorization': f'Bearer {env("NEW_TOKEN")}'}

class helper:

    def obtener_clientes_select():
        #obtener todos los clientes
        headers = crear_cabecera()
        response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/clientes', headers=headers)
        clientes = response.json()

        lista_clientes = [("","Ninguna")]
        for cliente in clientes:
            lista_clientes.append((cliente['id'], cliente['nombre']))
        return lista_clientes

    def obtener_habitaciones_select():
        #obtener todas las habitaciones
        headers = crear_cabecera()
        response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/habitaciones', headers=headers)
        habitaciones = response.json()

        lista_habitaciones = [("","Ninguna")]
        for habitacion in habitaciones:
            lista_habitaciones.append((habitacion['id'], habitacion['nombre']))
        return lista_habitaciones