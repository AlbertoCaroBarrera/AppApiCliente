from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('clientes',views.clientes_lista_api,name = 'clientes_lista_api')
]

