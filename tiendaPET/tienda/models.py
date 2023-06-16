from django.db import models

# Create your models here.

class Mascotas(models.Model):
    id=models.AutoField(db_column='id', primary_key=True)
    especie=models.CharField(blank=False, max_length=50, null=False)

    def __str__(self):
        return str(self.especie)

class Categoria(models.Model):
    id=models.AutoField(db_column='id', primary_key=True)
    nombre=models.CharField(blank=False, max_length=50, null=False)

    def __str__(self):
        return str(self.nombre)

class Productos(models.Model):
    id=models.AutoField(db_column='id', primary_key=True)
    nombre=models.CharField(blank=False, max_length=100, null=False)
    precio=models.IntegerField(blank=False, null=False)
    imagen=models.CharField(blank=False,max_length=255, null=false)
    mascotaId=models.ForeignKey('Mascota', on_delete=models.CASCADE, db_column='id')
    stock=models.IntegerField(blank=False)
    categoria_id=models.ForeignKey('Categoria', on_delete=models.CASCADE, db_column='id')

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    id=models.AutoField(db_column='id', primary_key=True)
    clienteId=models.ForeignKey('Cliente', on_delete=models.CASCADE, db_column='id')
    valorTotal=models.IntegerField(blank=false, default=0)

class Region(models.Model):
    cutReg=models.IntegerField(db_column='cut_reg', primary_key=True)
    nombre=models.CharField(blank=False, db_column='nombre')
    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    cutProv=models.IntegerField(db_column='cut_prov', primary_key=True)
    nombre=models.CharField(blank=False, db_column='nombre')
    cutReg=Models.ForeingKey('Region', on_delete=models.CASCADE, db_column='cut_reg') 
    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    cutCom=models.IntegerField(db_column='cut_com', primary_key=True)
    nombre=models.CharField(blank=False, db_column='nombre')
    cutProv=Models.ForeingKey('Provincia', on_delete=models.CASCADE, db_column='cut_prov')
    cutReg=Models.ForeingKey('Provincia', on_delete=models.CASCADE, db_column='cut_reg') 
    def __str__(self):
        return self.nombre

class Clientes(models.Model):
    id=models.AutoField(db_column=id, primary_key=True)
    rut=models.IntegerField(blank=False, null=False)
    dv=models.CharField(blank=False, max_length=1, null=False)
    primerApellido=models.CharField(blank=False, max_length=100, null=False)    
    segundoApellido=models.CharField(blank=True, max_length=100, null=True)
    direccion=models.CharField(blank=False, max_length=100, null=False)
    cutCom=models.IntegerField('Comuna', on_delete=models.CASCADE, db_colum='cut_com')
    cutProv=Models.ForeingKey('Comuna', on_delete=models.CASCADE, db_column='cut_prov')
    cutReg=Models.ForeingKey('Comuna', on_delete=models.CASCADE, db_column='cut_reg') 
    def __str__(self):
        return self.rut + self.dv

class Donantes(models.Model):
    id=models.AutoField(db_column=id, primary_key=True)
    rut=models.IntegerField(blank=False, null=False)
    dv=models.CharField(blank=False, max_length=1, null=False)
    primerApellido=models.CharField(blank=False, max_length=100, null=False)    
    segundoApellido=models.CharField(blank=True, max_length=100, null=True)
    direccion=models.CharField(blank=False, max_length=100, null=False)
    def __str__(self):
        return self.rut + self.dv
class Usuarios(models.Model):
    id=models.AutoField(db_column=id, primary_key=True)
    email=models.CharField(blank=False, max_length=100, null=False)
    password=models.CharField(blank=False, max_length=255, null=False)
    clienteId=models.ForeignKey('Clientes', on_delete=models.CASCADE, db_column='clientes_id')