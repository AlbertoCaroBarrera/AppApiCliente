from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('usuarios', views.usuarios_lista_api, name='usuarios_lista_api'),
    path('clientes', views.clientes_lista_api, name='clientes_lista_api'),
    path('clientes-mejorado', views.clientes_lista_api_mejorada, name='clientes_lista_api_mejorada'),
    path('clientes_lista_api', views.clientes_lista_api, name='clientes_lista_api'),
    path('cliente_busqueda_simple', views.cliente_busqueda_simple, name='cliente_busqueda_simple'),
    path('cliente_busqueda_avanzada', views.cliente_busqueda_avanzada, name='cliente_busqueda_avanzada'),
    path('habitaciones', views.habitaciones_lista_api, name='habitaciones_lista_api'),
    path('habitaciones-mejorado', views.habitaciones_lista_api_mejorada, name='habitaciones_lista_api_mejorada'),
    path('habitacion_busqueda_avanzada', views.habitacion_busqueda_avanzada, name='habitacion_busqueda_avanzada'),
    path('reservas', views.reservas_lista_api, name='reservas_lista_api'),
    path('reservas_lista_api', views.reservas_lista_api, name='reservas_lista_api'),
    path('reservas-mejorado', views.reservas_lista_api_mejorada, name='reservas_lista_api_mejorada'),
    path('reserva_busqueda_avanzada', views.reserva_busqueda_avanzada, name='reserva_busqueda_avanzada'),
    path('reservas/crear',views.reservas_crear,name='reserva_crear'),
]