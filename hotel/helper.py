
import requests
import environ
import os
from pathlib import Path
from datetime import datetime
from dateutil.parser import parse
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

    def obtener_clientes_select(request):
        #obtener todos los clientes
        headers = crear_cabecera_cliente(request)
        response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/clientes', headers=headers)
        clientes = response.json()
        lista_clientes = [("","Ninguna")]
        for cliente in clientes:
            lista_clientes.append((cliente['id'], cliente['nombre']))
        return lista_clientes

    def obtener_id_cliente(id,request):
        headers = crear_cabecera_cliente(request)
        response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/clientes', headers=headers)
        clientes = response.json()
        usuario = ""
        for cliente in clientes:
            if cliente['usuario'] == int(id):
                usuario = str(cliente['id'])
                break
        return usuario
        
    def obtener_nombre(id,request):
        headers = crear_cabecera_cliente(request)
        response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/clientes', headers=headers)
        clientes = response.json()
        usuario = ""
        for cliente in clientes:
            if cliente['usuario'] == int(id):
                usuario = cliente['nombre']
                break
        return usuario

        
    def obtener_habitaciones_select(request):
        #obtener todas las habitaciones
        headers = crear_cabecera_cliente(request)
        response = requests.get(f'{env("DOMINIO")}{env("VERSION")}/habitaciones', headers=headers)
        habitaciones = response.json()

        lista_habitaciones = [("","Ninguna")]
        for habitacion in habitaciones:
            lista_habitaciones.append((habitacion['id'], habitacion['tipo']))
        return lista_habitaciones
    
    def obtener_reserva(id,request):
        # obtenemos todos las reservas
        headers = crear_cabecera_cliente(request)
        response = requests.get(f'{env("DOMINIO")}/api/v1/reserva/'+str(id),headers=headers)
        reserva = response.json()
        return reserva
    
    def obtener_cliente(id,request):
        # obtenemos todos las clientees
        headers = crear_cabecera_cliente(request)
        response = requests.get(f'{env("DOMINIO")}/api/v1/cliente/'+str(id),headers=headers)
        cliente = response.json()
        return cliente

    def obtener_habitacion(id,request):
        # obtenemos todos las habitaciones
        headers = crear_cabecera_cliente(request)
        response = requests.get(f'{env("DOMINIO")}/api/v1/habitacion/'+str(id),headers=headers)
        habitacion = response.json()
        return habitacion
    

    def obtener_token_session(usuario,password):
        token_url = f'{env("DOMINIO")}/oauth2/token/'
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
        
    def obtener_habitacion_select(request):
        headers = crear_cabecera_cliente(request)
        response = requests.get(f'{env("DOMINIO")}' + 'habitaciones',headers=headers)
        habitaciones = response.json()
        
        lista_habitaciones = []
        for habitacion in habitaciones:
            lista_habitaciones.append((habitacion["id"],habitacion["numero_hab"]))
        return lista_habitaciones
    
    def es_aniversario(fecha_registro):
        fecha_actual = parse(str(datetime.now()))

        fecha_registro = parse(str(fecha_registro))

        if fecha_actual.month == fecha_registro.month and fecha_actual.day == fecha_registro.day:
            return True
        else:
            return False
        
    def imagenes():
        imagenes =     [
    "https://media.istockphoto.com/id/1392278298/es/foto/vista-a-un-nuevo-apartamento-de-hotel-restaurado-con-ba%C3%B1o.jpg?s=612x612&w=0&k=20&c=85t7iCyi3s9jR-U1WlgmRowQpjxSq96x8OsVm83Hxn0=",
    "https://media.istockphoto.com/id/1392277376/es/foto/interior-de-una-habitaci%C3%B3n-de-hotel-de-lujo.jpg?s=612x612&w=0&k=20&c=x78jEAQ7NpajoERxSllN4iDJ2eARFUNrDnIqCtl92Gc=",
    "https://media.istockphoto.com/id/502386716/es/foto/moderno-interior-de-un-dormitorio.jpg?s=612x612&w=0&k=20&c=4-J2WdcSk5QGmg2XX_ofCJ1OdHwbTfdknw3Ts4cIf7I=",
    "https://media.istockphoto.com/id/492586662/es/foto/de-ba%C3%B1o.jpg?s=612x612&w=0&k=20&c=DZN9VKWyoqTj4krYv70hXkp0IRymJZLj8gFI5MVB4D0=",
    "https://media.istockphoto.com/id/511725130/es/foto/de-recepci%C3%B3n-de-madera-con-%C3%A1rea-de-recepci%C3%B3n.jpg?s=612x612&w=0&k=20&c=c8r40NgsDY8WDWath58j6UCj3UHnBsDb8XgX89l_xGY=",
    "https://media.istockphoto.com/id/517715815/es/foto/lobby-interior-con-caf%C3%A9-visible-a-trav%C3%A9s-de-un-panel-de-vidrio.jpg?s=612x612&w=0&k=20&c=-eV1zQLGHErhPPtkE3lje6R72t2UBj6hqdQMhDWeZQ8=",
    "https://media.istockphoto.com/id/539980310/es/foto/corredor-en-un-crucero.jpg?s=612x612&w=0&k=20&c=Cxz-rujVhdjgQ_szleYe3KZw-1ssKYoOuB_4jptqB_Y=",
    "https://media.istockphoto.com/id/179264087/es/foto/moderno-interior.jpg?s=612x612&w=0&k=20&c=yeBngkG3qkzL74i0bkpnbqOCWwFeDFpvCtejONUvtgU=",
    "https://media.istockphoto.com/id/690819570/es/foto/ilustraci%C3%B3n-3d-de-interior-moderno-hotel-corredor.jpg?s=612x612&w=0&k=20&c=DKQdymkzkQut1bDN-FzRfJ31f42K8z17wr0FxfDFfuE=",
    "https://media.istockphoto.com/id/1355726436/es/foto/moderno-interior-de-ba%C3%B1o-de-lujo-con-jacuzzi-y-hermosas-vistas-al-mar.jpg?s=612x612&w=0&k=20&c=1A83WpSKV6Joc7Bd36oTHEsYuezuOhLDTCTyHB5m-v8=",
    "https://media.istockphoto.com/id/1163500692/es/foto/interior-de-un-pasillo-de-hotel-de-m%C3%A1rmol-brillante-con-ascensor.jpg?s=612x612&w=0&k=20&c=0K1JiXEyBYlZqAij6X_KcEDJByG68IMYg186xOouEwY=",
    "https://media.istockphoto.com/id/1828065319/es/foto/iluminaci%C3%B3n-de-pasillos.jpg?s=612x612&w=0&k=20&c=k2ZdlaKtQUuEAFKprRBaDktEJ4VjNzqblhICwZaL0Ko=",
    "https://media.istockphoto.com/id/851575804/es/foto/centro-de-spa-del-hotel.jpg?s=612x612&w=0&k=20&c=IYSOVT48C3YQ31Wp3bJ_vW7u2F14Oa0Fm6udlUA5Qnc=",
    "https://media.istockphoto.com/id/176002959/es/foto/temprano-en-la-ma%C3%B1ana-al-corredor.jpg?s=612x612&w=0&k=20&c=HshknO3ZVdEPLFooNZqLaqf7VINeVxcGoaz4HWq7580=",
    "https://media.istockphoto.com/id/1126700951/es/foto/3d-render-postmodernista-interior-living-comedor-hogar.jpg?s=612x612&w=0&k=20&c=m2aFW37I_UlK-7HJrNZUm5InFrh_dD_e923WkBIscwE=",
    "https://media.istockphoto.com/id/1429098510/es/foto/pasillo-con-suelo-de-m%C3%A1rmol-en-habitaci%C3%B3n-de-hotel-de-lujo.jpg?s=612x612&w=0&k=20&c=ieSo3UUVeax7Sofft8Il-Qj-_J9umi3O2kCEJQjPccE=",
    "https://media.istockphoto.com/id/1040614368/es/foto/interior-de-la-vivienda-tonos-c%C3%A1lidos-suelos-de-madera-armario-empotrado.jpg?s=612x612&w=0&k=20&c=m473CgoXYqAnI2vugKZl3mokhv3FMHaus7TwviRLHuc=",
    "https://media.istockphoto.com/id/183260138/es/foto/entrada-de-la-oficina-moderna-con-asiento-y-maxi-pantalla.jpg?s=612x612&w=0&k=20&c=4IUuqc97JxCPwXCQuQMXs_zjYgcBAmH5mkUcDz9o28Y=",
    "https://media.istockphoto.com/id/1476745782/es/foto/corredor-del-hotel.jpg?s=612x612&w=0&k=20&c=1B9NUhGY5EUjoIHGZjn93wD4uvMtLGYhePVQQHMvt5s=",
    "https://media.istockphoto.com/id/157591223/es/foto/oficinas-de-corporate-executive.jpg?s=612x612&w=0&k=20&c=KB_X4Fubv5h0RM8u3b0UWHiVhrr0Kz2LBSTmHCsOyGg=",
    "https://media.istockphoto.com/id/1392325744/es/foto/interior-del-pasillo-de-oficinas-de-estilo-moderno.jpg?s=612x612&w=0&k=20&c=DUgvvFfy95V4MoclcE5V7W9mJzD6_D-9HQACx6cYz4M=",
    "https://media.istockphoto.com/id/619261436/es/foto/moderno-pasillo-del-vest%C3%ADbulo-en-el-estilo-contempor%C3%A1neo.jpg?s=612x612&w=0&k=20&c=E_zE8CWm9j32B-sO9jZxmb34XWxVeJhnVTW4BiKA8B8=",
    "https://media.istockphoto.com/id/539672910/es/foto/habitaci%C3%B3n-de-oficina.jpg?s=612x612&w=0&k=20&c=ef6NWBmJXqKm6_W_jLSqzIve9L1uqmHWWe8b9fLrF4c=",
    "https://media.istockphoto.com/id/953006244/es/foto/interior-liso-de-sal%C3%B3n-pasillo-con-puerta-abierta.jpg?s=612x612&w=0&k=20&c=f9tQtxZ8Cpv_Zxg6d4J1ZEF8PdwKZtSzb025drxyaGM=",
    "https://media.istockphoto.com/id/523487416/es/foto/blanco-de-la-sala-de-estar-en-casa-moderna-interior.jpg?s=612x612&w=0&k=20&c=F6jyOl74RzXGgDpULW1IjDl29luU7u5ljg5jVLk6048=",
    "https://media.istockphoto.com/id/1316450473/es/foto/condominio-vac%C3%ADo-hotel-o-pasillo-de-apartamentos-camino-en-edificio-de-condominios-moderna.jpg?s=612x612&w=0&k=20&c=6HONodFIFBMaGexhZcT7TG4UNtfwGezrNvv7E_wdVW4=",
    "https://media.istockphoto.com/id/810003150/es/foto/renderizado-3d-de-un-dise%C3%B1o-interior-de-ba%C3%B1o.jpg?s=612x612&w=0&k=20&c=Nqxl8-ee7EqCYKbhU8VnijqaQoyySMYAgfUDQ3Eo5aQ=",
    "https://media.istockphoto.com/id/1410955429/es/foto/%C3%A1rea-de-trabajo-en-oficina-moderna-con-piso-de-alfombra-y-sala-de-reuniones.jpg?s=612x612&w=0&k=20&c=uY2al5q3RxqX6W8ud01HhvkFt1d04cecU3JQKsCPMts=",
    "https://media.istockphoto.com/id/183382162/es/foto/ascensor-del-lobby.jpg?s=612x612&w=0&k=20&c=j7qoY_W3LmGPqHC94oqZdcpQM_OsM2hm0o2gH_Xxjo4=",
    "https://media.istockphoto.com/id/1429222265/es/foto/ilustraci%C3%B3n-3d-del-dise%C3%B1o-interior-del-pasillo-en-un-estilo-de-madera-renderizado-3d-del.jpg?s=612x612&w=0&k=20&c=LYNFARFfpxPS-W9irxUNBKvSoX5DJa6ejPHJDmMR9BQ=",
    "https://media.istockphoto.com/id/833247136/es/foto/pasillo-de-la-entrada-de-hotel-habitaci%C3%B3n.jpg?s=612x612&w=0&k=20&c=4PutskBzm-TOQ671ZHXWS-2oUmtZM6Ux3boFxh8AGq0=",
    "https://media.istockphoto.com/id/585180182/es/foto/lujo-moderno-lobby-del-hotel.jpg?s=612x612&w=0&k=20&c=Hz7ckOEo65JyzL8shpnCuKp4z6w6dT0GuCk25Zo9xpY=",
    "https://media.istockphoto.com/id/1326747642/es/foto/renderizado-3d-interior-cama-vac%C3%ADa-aislada-en-el-hospital-primer-plano-en-la-cama-abandonada.jpg?s=612x612&w=0&k=20&c=b2BB5jEf73-xApeby5la5xNRurcuISmFp9zj44Xeqr0=",
    "https://media.istockphoto.com/id/139702949/es/foto/japon%C3%A9s-con-piso-tatami.jpg?s=612x612&w=0&k=20&c=KRmqO_u-DRGbMhpryUGAqc8QXb8uyTGfiQv0ZShsUkc=",
    "https://media.istockphoto.com/id/1253241310/es/foto/estilo-ryokan-de-la-posada-tradicional-japonesa.jpg?s=612x612&w=0&k=20&c=Lo-Nrzjrez7JNvZ7K-7yOBpQ57Xy3nWv1rsl91AuN9s=",
    "https://media.istockphoto.com/id/472402278/es/foto/moderno-interior-de-antesala.jpg?s=612x612&w=0&k=20&c=gEjhrD6MncYi3HHsZdclez3K3rol_kPqIH8_gq3mLTw=",
    "https://media.istockphoto.com/id/1175598327/es/foto/hombre-de-negocios-con-equipaje-con-ruedas-en-suite.jpg?s=612x612&w=0&k=20&c=UDrcAtMwuLK4vs2uUiY7XMxpQUJ7dT7oOQ4ZtNXqVZ0=",
    "https://media.istockphoto.com/id/1190885424/es/foto/3d-render-de-interior-de-sala-de-estar-moderna.jpg?s=612x612&w=0&k=20&c=f0EeuN9tiF7PcEc6z63MoPy9aCSEi_4abjT4qRKHJgs=",
    "https://media.istockphoto.com/id/523272949/es/foto/arquitectura-moderna-zona.jpg?s=612x612&w=0&k=20&c=aGHwLF3rlvTYFC2s2NkcjBF94Cdc8jCA4rjonYRyUew=",
    "https://media.istockphoto.com/id/1389025951/es/foto/3d-render-de-ba%C3%B1o-de-lujo.jpg?s=612x612&w=0&k=20&c=pj-2KhMfLxIi_spnmYyFe1j7v5YXSxoYW-YOOfNrNJc=",
    "https://media.istockphoto.com/id/526658373/es/foto/cafe-en-el-moderno-edificio-de-oficinas.jpg?s=612x612&w=0&k=20&c=w5T9TJ146E4K-HrnDaeHYEhTVY8bnyhQaqMwyQRBCDo=",
    "https://media.istockphoto.com/id/1164135387/es/foto/dise%C3%B1o-interior-del-sitio-de-construcci%C3%B3n-en-proceso-de-renovaci%C3%B3n.jpg?s=612x612&w=0&k=20&c=_5D9NCyMEhB-zw-pBt0gN8j8SpiSX81DdrrTUDfJxCo=",
    "https://media.istockphoto.com/id/1348027809/es/foto/ba%C3%B1o-moderno.jpg?s=612x612&w=0&k=20&c=goU79HT03r0TFKN5qrtVRVXshEDop6Og84I4ldzFUh4=",
    "https://media.istockphoto.com/id/1207917497/es/foto/peque%C3%B1a-habitaci%C3%B3n-de-hotel-de-lujo-con-puerta-abierta-al-ba%C3%B1o-y-armario-de-madera-en-el.jpg?s=612x612&w=0&k=20&c=oQsHk1XAzabiVsgRhY7JHamWfsmTAVunLBV1AvXMGXo=",
    "https://media.istockphoto.com/id/1310344430/es/foto/representaci%C3%B3n-en-3d-de-la-exposici%C3%B3n-de-la-tienda.jpg?s=612x612&w=0&k=20&c=QkslgoTygB2b14_VAlvIC-_ovKRE8_lUaJ7SSkwW5AE=",
    "https://media.istockphoto.com/id/804600872/es/foto/sillas-y-mesa-en-corredor-moderno.jpg?s=612x612&w=0&k=20&c=oyx6zeUZdtz-hXXb4hIEMG9WuSRDhmXvcbXrz7mfKQw=",
    "https://media.istockphoto.com/id/146723343/es/foto/colorido-oficina-lobby.jpg?s=612x612&w=0&k=20&c=9ENalhqAmxF1dTO4VZL1fERY5NBBfu8p4OIpdgnNW1E=",
    "https://media.istockphoto.com/id/1134267286/es/foto/acogedora-sala-de-recepci%C3%B3n-de-yoga-y-centro-de-bienestar.jpg?s=612x612&w=0&k=20&c=_ExqasNg_mBUrgR2c4NUgT3DDDIhInGo-9KcdHLxiC4=",
    "https://media.istockphoto.com/id/1159903153/es/foto/3d-render-del-interior-de-la-entrada-del-vest%C3%ADbulo-del-hotel-de-lujo.jpg?s=612x612&w=0&k=20&c=EdbKdgpUCd_C6E5OArQZud4UEjrvIyRwoKXF7HH3vX4=",
    "https://media.istockphoto.com/id/1758891965/es/foto/armario-moderno-con-elegantes-ropas-y-accesorios-de-primavera.jpg?s=612x612&w=0&k=20&c=WMDAk5gbLAdCkOteYI54-cYTIISDUirZC508L6NL9E0=",
    "https://media.istockphoto.com/id/1391120866/es/foto/render-3d-de-sala-de-estar-moderna.jpg?s=612x612&w=0&k=20&c=imF-Mau1FuB2OBzCwoiWDtXWN0zoCU0q_HC35d2Py0w=",
    "https://media.istockphoto.com/id/1177651744/es/foto/suite-de-hotel-3d-render-con-ba%C3%B1o-de-lujo.jpg?s=612x612&w=0&k=20&c=nUbuDtcvYf_-Y2Ju4e1D3P0S39CpL4VOFPLut55KD8Y=",
    "https://media.istockphoto.com/id/145988555/es/foto/interior-de-la-oficina-moderna.jpg?s=612x612&w=0&k=20&c=6JHZgOqTREo7kcYhhYdj44u0OaYZkOOHyshw3B0tJNA=",
    "https://media.istockphoto.com/id/1163207573/es/foto/3d-render-del-vest%C3%ADbulo-y-recepci%C3%B3n-del-hotel-de-lujo.jpg?s=612x612&w=0&k=20&c=rgwi66rz4Ne-muEbTJkJFzg6qwItiInWwxmHMuXe6R8=",
    "https://media.istockphoto.com/id/1306218458/es/foto/fragmento-del-interior-del-pasillo-y-sala-de-estar-en-el-apartamento.jpg?s=612x612&w=0&k=20&c=PgLziBi9F8t1QMpo05HsBMrcT5PNLuw8V9iFvG919dM=",
    "https://media.istockphoto.com/id/1392278022/es/foto/interior-de-una-habitaci%C3%B3n-de-hotel-de-lujo-mesa-de-madera-montada-en-la-pared.jpg?s=612x612&w=0&k=20&c=Z9B4eak5wYxLhSs1FjzWAD8SSP0eLbeH2UP_FgsQ_7o=",
    "https://media.istockphoto.com/id/528982807/es/foto/el-interior-de-la-c%C3%A1mara-de-entrada.jpg?s=612x612&w=0&k=20&c=YGXbVqAV9ZXdtjFgMFA4cENt0GV8baUi7O4nwKoQ--g=",
]
        longitud_subgrupo = len(imagenes) // 4 
        imagenes_grupo1 = imagenes[:longitud_subgrupo]
        imagenes_grupo2 = imagenes[longitud_subgrupo:longitud_subgrupo*2]
        imagenes_grupo3 = imagenes[longitud_subgrupo*2:longitud_subgrupo*3]
        imagenes_grupo4 = imagenes[longitud_subgrupo*3:]

        return  {
            'pequeña': imagenes_grupo1,
            'mediana': imagenes_grupo2,
            'grande': imagenes_grupo3,
            'deluxe': imagenes_grupo4,
        }