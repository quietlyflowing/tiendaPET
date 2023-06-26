from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils.html import mark_safe
from .models import Productos
# Create your views here.

def index(request):
    products = Productos.objects.order_by('-conteoVistas')[:6]
    context = {"jumbotron_titulo": "Somos TiendaPET", "jumbotron_subtitulo": "Tenemos los mejores productos para tu mascota", "jumbotron_fondo": 'tienda/img/boxer.jpg', "jumbotron_opt": mark_safe('<button class="btn btn-primary btn-lg" type="button" data-bs-toggle="modal" data-bs-target="#modalNosotros">Sobre Nosotros</button>')}
    for i in range(6):
        context['producto{}_id'.format(i+1)] = products[i].id
        context['producto{}_nombre'.format(i+1)] = products[i].nombre
        context['producto{}_precio'.format(i+1)] = products[i].precio
        context['producto{}_imagen'.format(i+1)] = products[i].imagen
    template = loader.get_template("index.html")
    return HttpResponse(template.render(context,request))

def cats(request):
    products = Productos.objects.filter(mascota=1)
    template = loader.get_template("gallery.html")
    context = {"Productos": products, "titulo_galeria": "Gatos", "jumbotron_titulo": "Productos para Gatos", "jumbotron_subtitulo": "¡Todo para los reyes del hogar!", "jumbotron_fondo": 'tienda/img/kitten.jpg'}
    return HttpResponse(template.render(context, request))

def dogs(request):
    products = Productos.objects.filter(mascota=2)
    template = loader.get_template("gallery.html")
    context = {"Productos": products, "titulo_galeria": "Perros", "jumbotron_titulo": "Productos para Perros", "jumbotron_subtitulo": "¡Todo para el mejor amigo del hombre!", "jumbotron_fondo": 'tienda/img/terrier.jpg'}
    return HttpResponse(template.render(context, request))

def contact(request):
    template = loader.get_template("contacto.html")
    context = {}
    return HttpResponse(template.render(context, request))
    