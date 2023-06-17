from django.db import models

# Create your models here.
class Categorias(models.Model):
    nombre=models.CharField(blank=False, max_length=50, null=False)

    def __str__(self):
        return str(self.nombre)

class Mascotas(models.Model):
    especie=models.CharField(blank=False, max_length=50, null=False)

    def __str__(self):
        return str(self.especie)

class Regiones(models.Model):
    cutReg=models.IntegerField(db_column='cut_reg', primary_key=True)
    nombre=models.CharField(blank=False, db_column='nombre', max_length=100)
    def __str__(self):
        return self.nombre

class Provincias(models.Model):
    cutProv=models.IntegerField(db_column='cut_prov', primary_key=True)
    nombre=models.CharField(blank=False, max_length=100)
    region=models.ForeignKey('Regiones', on_delete=models.CASCADE) 
    def __str__(self):
        return self.nombre

class Comunas(models.Model):
    cutCom=models.IntegerField(db_column='cut_com', primary_key=True)
    nombre=models.CharField(blank=False, db_column='nombre', max_length=50)
    provincia=models.ForeignKey('Provincias', on_delete=models.CASCADE)
    regionProv=models.ForeignKey('Regiones', on_delete=models.CASCADE) 
    def __str__(self):
        return self.nombre

class Productos(models.Model):
    nombre=models.CharField(blank=False, max_length=100, null=False)
    precio=models.IntegerField(blank=False, null=False)
    imagen=models.CharField(blank=False,max_length=255, null=False)
    mascotaId=models.ForeignKey('Mascotas', on_delete=models.CASCADE)
    stock=models.IntegerField(blank=False)
    categoria_id=models.ForeignKey('Categorias', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    clienteId=models.ForeignKey('Clientes', on_delete=models.CASCADE)
    valorTotal=models.IntegerField(blank=False, default=0)


class Clientes(models.Model):
    rut=models.IntegerField(blank=False, null=False)
    dv=models.CharField(blank=False, max_length=1, null=False)
    primerApellido=models.CharField(blank=False, max_length=100, null=False)    
    segundoApellido=models.CharField(blank=True, max_length=100, null=True)
    direccion=models.CharField(blank=False, max_length=100, null=False)
    comId=models.ForeignKey('Comunas', on_delete=models.CASCADE)
    # provId=models.ForeignKey('Comunas', on_delete=models.CASCADE)
    # cutReg=models.ForeignKey('Comunas', on_delete=models.CASCADE) 
    def __str__(self):
        return self.rut + self.dv

class Donantes(models.Model):
    rut=models.IntegerField(blank=False, null=False)
    dv=models.CharField(blank=False, max_length=1, null=False)
    primerApellido=models.CharField(blank=False, max_length=100, null=False)    
    segundoApellido=models.CharField(blank=True, max_length=100, null=True)
    direccion=models.CharField(blank=False, max_length=100, null=False)
    def __str__(self):
        return self.rut + self.dv

class Usuarios(models.Model):
    email=models.CharField(blank=False, max_length=100, null=False)
    password=models.CharField(blank=False, max_length=255, null=False)
    clienteId=models.ForeignKey('Clientes', on_delete=models.CASCADE)