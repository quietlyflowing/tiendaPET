from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Regiones)
admin.site.register(Provincias)   #new
admin.site.register(Comunas)
admin.site.register(Categorias)
admin.site.register(Productos)   #new
admin.site.register(Mascotas)
admin.site.register(DetalleCarrito)
admin.site.register(Clientes)   #new
admin.site.register(Donantes)
admin.site.register(MensajesContacto)   