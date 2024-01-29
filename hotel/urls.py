from django.urls import path
from .import views
urlpatterns = [
    path('clientes', views.clientes_lista_api, name='clientes_lista_api'),
    path('reservas', views.reservas_lista_api, name='reservas_lista_api'),
    path('usuarios', views.usuarios_lista_api, name='usuarios_lista_api'),
    path('habitaciones', views.habitaciones_lista_api, name='habitaciones_lista_api'),
    path('reservas-mejorado', views.reservas_lista_api_mejorada, name='reservas_lista_api_mejorada'),
    path('clientes-mejorado', views.clientes_lista_api_mejorada, name='clientes_lista_api_mejorada'),
    path('usuarios-mejorado', views.usuarios_lista_api_mejorada, name='usuarios_lista_api_mejorada'),
    path('habitaciones-mejorado', views.habitaciones_lista_api_mejorada, name='habitaciones_lista_api_mejorada'),

]

