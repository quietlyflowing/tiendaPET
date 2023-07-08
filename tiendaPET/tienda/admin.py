from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Region)
admin.site.register(Provincia)   #new
admin.site.register(Comuna)
admin.site.register(Categoria)
admin.site.register(Producto)   #new
admin.site.register(Mascota)
admin.site.register(DetalleCarrito)
admin.site.register(Cliente)   #new
admin.site.register(Donante)
admin.site.register(MensajesContacto)   