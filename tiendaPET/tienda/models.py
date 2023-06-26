from django.db import models

# Create your models here.
class Categorias(models.Model):
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(blank=False, max_length=50, null=False)


class Mascotas(models.Model):
    especie=models.CharField(blank=False, max_length=50, null=False)


class Regiones(models.Model):
    nombre=models.CharField(blank=False, max_length=250)
    numeralRomano=models.CharField(blank=False, max_length=2, db_column='numeral_romano')

class Provincias(models.Model):
    nombre=models.CharField(blank=False, max_length=255)
    region=models.ForeignKey('Regiones', on_delete=models.CASCADE) 

class Comunas(models.Model):
    nombre=models.CharField(blank=False, max_length=255)
    provincia=models.ForeignKey('Provincias', on_delete=models.CASCADE)

class Productos(models.Model):
    nombre=models.CharField(blank=False, max_length=100, null=False)
    precio=models.IntegerField(blank=False, null=False)
    imagen=models.CharField(blank=False,max_length=255, null=False)
    mascota=models.ForeignKey('Mascotas', on_delete=models.CASCADE)
    stock=models.IntegerField(blank=False)
    categoria=models.ForeignKey('Categorias', on_delete=models.CASCADE)
    descripcion=models.TextField(blank=False, max_length=350, null=False, default="Lorem Ipsum Dolor Sit Amen")
    conteoVistas=models.IntegerField(blank=False, default=0, db_column='conteo_vistas',null=False)

class Carrito(models.Model):
    cliente=models.ForeignKey('Clientes', on_delete=models.CASCADE, null=True)
    valorTotal=models.IntegerField(blank=False, default=0)


class Clientes(models.Model):
    rut=models.IntegerField(blank=False, null=False)
    dv=models.CharField(blank=False, max_length=1, null=False)
    primerApellido=models.CharField(blank=False, max_length=100, null=False)    
    segundoApellido=models.CharField(blank=True, max_length=100, null=True)
    direccion=models.CharField(blank=False, max_length=100, null=False)
    comuna=models.ForeignKey('Comunas', on_delete=models.CASCADE)


class Donantes(models.Model):
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
