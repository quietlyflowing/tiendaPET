from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    template = loader.get_template("index.html")
    context = {}
    return HttpResponse(template.render(context,request))

def cats(request):
    template = loader.get_template("gatos.html")
    context = {}
    return HttpResponse(template.render(context, request))

def dogs(request):
    template = loader.get_template("perros.html")
    context = {}
    return HttpResponse(template.render(context, request))

def contact(request):
    template = loader.get_template("contacto.html")
    context = {}
    return HttpResponse(template.render(context, request))