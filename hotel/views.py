from django.shortcuts import render,redirect
from django.db.models import Q,Prefetch
from django.forms import modelform_factory
from .forms import *
from django.contrib import messages
import requests
from django.core import serializers
# Create your views here.
def index(request):
    return render(request,'index.html')

def clientes_lista_api(request):
    response = requests.get('http://127.0.0.1:8000/api/v1/clientes')
    clientes = response.json()
    return render(request, 'cliente/lista_api.html',{"clientes_mostrar":clientes})

def reservas_lista_api(request):
    response = requests.get('http://127.0.0.1:8000/api/v1/reservas')
    reservas = response.json()
    return render(request,'reserva/reserva_list.html',{"reservas_mostrar":reservas})