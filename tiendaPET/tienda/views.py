from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils.html import mark_safe

# Create your views here.

def index(request):
    template = loader.get_template("index.html")
    context = {"jumbotron_titulo": "Somos TiendaPET", "jumbotron_subtitulo": "Tenemos los mejores productos para tu mascota", "jumbotron_fondo": 'tienda/img/boxer.jpg', "jumbotron_opt": mark_safe('<button class="btn btn-primary btn-lg" type="button" data-bs-toggle="modal" data-bs-target="#modalNosotros">Sobre Nosotros</button>')}
    return HttpResponse(template.render(context,request))

def cats(request):
    template = loader.get_template("gatos.html")
    context = {"jumbotron_titulo": "Productos para Gatos", "jumbotron_subtitulo": "¡Todo para los reyes del hogar!", "jumbotron_fondo": 'tienda/img/kitten.jpg'}
    return HttpResponse(template.render(context, request))

def dogs(request):
    template = loader.get_template("perros.html")
    context = {"jumbotron_titulo": "Productos para Perros", "jumbotron_subtitulo": "¡Todo para el mejor amigo del hombre!", "jumbotron_fondo": 'tienda/img/terrier.jpg'}
    return HttpResponse(template.render(context, request))

def contact(request):
    template = loader.get_template("contacto.html")
    context = {}
    return HttpResponse(template.render(context, request))