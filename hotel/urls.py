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
    path('clientes/crear',views.clientes_crear,name='cliente_crear'),
    path('cliente/editar/nombre/<int:cliente_id>',views.cliente_editar_nombre,name='cliente_editar_nombre'),
    
    path('cliente/editar/<int:cliente_id>',views.cliente_editar,name='cliente_editar'),
    
    path('cliente/eliminar/<int:cliente_id>',views.cliente_eliminar,name='cliente_eliminar'),
    
    
    path('habitaciones', views.habitaciones_lista_api, name='habitaciones_lista_api'),
    path('habitaciones-mejorado', views.habitaciones_lista_api_mejorada, name='habitaciones_lista_api_mejorada'),
    path('habitacion_busqueda_avanzada', views.habitacion_busqueda_avanzada, name='habitacion_busqueda_avanzada'),
    path('habitaciones/crear',views.Habitacion_crear,name='habitacion_crear'),
    path('habitacion/editar/<int:habitacion_id>',views.habitacion_editar,name='habitacion_editar'),
    path('habitacion/editar/nombre/<int:habitacion_id>',views.habitacion_editar_nombre,name='habitacion_editar_nombre'),
    path('habitacion/eliminar/<int:habitacion_id>',views.habitacion_eliminar,name='habitacion_eliminar'),
    
    
    
    path('reservas', views.reservas_lista_api, name='reservas_lista_api'),
    path('reservas_lista_api', views.reservas_lista_api, name='reserva_mostrar'),
    path('reservas-mejorado', views.reservas_lista_api_mejorada, name='reservas_lista_api_mejorada'),
    path('reserva_busqueda_avanzada', views.reserva_busqueda_avanzada, name='reserva_busqueda_avanzada'),
    path('reservas/crear',views.reservas_crear,name='reserva_crear'),
    path('reserva/editar/<int:reserva_id>',views.reserva_editar,name='reserva_editar'),
    path('reserva/editar/fecha/<int:reserva_id>',views.reserva_editar_fecha,name='reserva_editar_fecha'),
    path('reserva/eliminar/<int:reserva_id>',views.reserva_eliminar,name='reserva_eliminar'),
]