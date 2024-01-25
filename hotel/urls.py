from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('clientes',views.clientes_lista_api,name = 'clientes_lista_api'),
    path('reservas',views.reservas_lista_api,name = 'reservas_lista_api'),
    path('cliente_buscar',views.cliente_busqueda_simple,name='cliente_busqueda_simple'),
    path('cliente_busqueda_avanzada',views.cliente_busqueda_avanzada,name='cliente_busqueda_avanzada'),

]

