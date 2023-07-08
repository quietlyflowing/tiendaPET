from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager



class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# Create your models here.
class Categoria(models.Model):
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(blank=False, max_length=50, null=False)

    def __str__(self):
        return self.nombre


class Mascota(models.Model):
    especie=models.CharField(blank=False, max_length=50, null=False)
    def __str__(self):
        return self.especie

class Region(models.Model):
    nombre=models.CharField(blank=False, max_length=250)
    numeralRomano=models.CharField(blank=False, max_length=2, db_column='numeral_romano')
    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    nombre=models.CharField(blank=False, max_length=255)
    region=models.ForeignKey('Region', on_delete=models.CASCADE) 
    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre=models.CharField(blank=False, max_length=255)
    provincia=models.ForeignKey('Provincia', on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre=models.CharField(blank=False, max_length=100, null=False)
    precio=models.IntegerField(blank=False, null=False)
    imagen=models.CharField(blank=False,max_length=255, null=False)
    #imagen=models.ImageField(upload_to='img') //para posterior desarrollo
    mascota=models.ForeignKey('Mascota', on_delete=models.CASCADE)
    stock=models.IntegerField(blank=False)
    categoria=models.ForeignKey('Categoria', on_delete=models.CASCADE)
    descripcion=models.TextField(blank=False, max_length=350, null=False, default="Lorem Ipsum Dolor Sit Amen")
    conteoVistas=models.IntegerField(blank=False, default=0, db_column='conteo_vistas',null=False)
    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    cliente=models.ForeignKey('Cliente', on_delete=models.CASCADE, null=True)
    valorTotal=models.IntegerField(blank=False, default=0)


class Cliente(models.Model):
    rut=models.IntegerField(blank=False, null=False)
    dv=models.CharField(blank=False, max_length=1, null=False)
    primerApellido=models.CharField(blank=False, max_length=100, null=False)    
    segundoApellido=models.CharField(blank=True, max_length=100, null=True)
    direccion=models.CharField(blank=False, max_length=100, null=False)
    comuna=models.ForeignKey('Comuna', on_delete=models.CASCADE)
    usuario=models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True)

class DetalleCarrito(models.Model):
    producto=models.ForeignKey('Producto', on_delete=models.CASCADE)
    carrito=models.ForeignKey('Carrito', on_delete=models.CASCADE)
    cantidad=models.IntegerField(blank=False, null=False)
    precioTotal=models.IntegerField(blank=False, db_column="precio_total", null=False)


class Donante(models.Model):
    rut=models.IntegerField(blank=False, null=False)
    dv=models.CharField(blank=False, max_length=1, null=False)
    primerApellido=models.CharField(blank=False, max_length=100, null=False)    
    segundoApellido=models.CharField(blank=True, max_length=100, null=True)
    direccion=models.CharField(blank=False, max_length=100, null=False)

class MensajesContacto(models.Model):
    DUDA="DD"
    RECLAMO="RC"
    FELICITACION="FC"
    SUGERENCIA="SG"
    DEFAULT="DF"
    nombre=models.CharField(blank=False, max_length=100, null=False)
    email=models.CharField(blank=False, max_length=100, null=False)
    MOTIVO_CONSULTA_CHOICES = [(DUDA, "Duda"),
    (SUGERENCIA, "Sugerencia"),
    (RECLAMO, "Reclamo"),
    (FELICITACION, "Felicitación"),
    (DEFAULT, "Seleccione un motivo de consulta")]
    motivoContacto=models.CharField(max_length=2, choices=MOTIVO_CONSULTA_CHOICES, default=DEFAULT)
    message=models.TextField(blank=False, max_length=700, null=False)
