from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils.html import mark_safe
from .models import *
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.template.loader import render_to_string
from .forms import *
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.db.models import Sum, F
from django.core import serializers
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, update_session_auth_hash

# Create your views here.


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            try:
                carrito = request.user.cliente.carrito
            except ObjectDoesNotExist:
                carrito = Carrito.objects.create(cliente=cliente)
            return JsonResponse({'status':'success'}, status=200)
        else:
            return JsonResponse({'status':'invalid'}, status=400)

def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return JsonResponse({'status':'sucess'})

def index(request):
    if request.user.is_authenticated:
        if request.user.cliente.carrito is not None:
            cartQty = request.user.cliente.carrito.cantidadTotal
        else:
            cartQty = 0
    elif request.user.is_anonymous:
            cartQty = 0
    products = Producto.objects.order_by('-conteoVistas')[:6]
    context = { 
    'cart_cantidad': cartQty,
    "jumbotron_titulo": "Somos TiendaPET", 
    "jumbotron_subtitulo": "Tenemos los mejores productos para tu mascota",
    "jumbotron_fondo": 'tienda/img/boxer.jpg', 
    "jumbotron_opt": mark_safe('<button class="btn btn-primary btn-lg" type="button" data-bs-toggle="modal" data-bs-target="#modalNosotros">Sobre Nosotros</button>')}
    for i in range(6):
        context['producto{}_id'.format(i+1)] = products[i].id
        context['producto{}_nombre'.format(i+1)] = products[i].nombre
        context['producto{}_precio'.format(i+1)] = products[i].precio
        context['producto{}_imagen'.format(i+1)] = products[i].imagen
    template = loader.get_template("index.html")
    return HttpResponse(template.render(context,request))
        
def cats(request):
    if request.user.is_authenticated:
        if request.user.cliente.carrito is not None:
            cartQty = request.user.cliente.carrito.cantidadTotal
        else:
            cartQty = 0
    elif request.user.is_anonymous:
            cartQty = 0
    products = Producto.objects.filter(mascota=1)
    template = loader.get_template("gallery.html")
    context = {"cart_cantidad": cartQty, "Productos": products, "titulo_galeria": "Gatos", "jumbotron_titulo": "Productos para Gatos", "jumbotron_subtitulo": "¡Todo para los reyes del hogar!", "jumbotron_fondo": 'tienda/img/kitten.jpg'}
    return HttpResponse(template.render(context, request))

def dogs(request):
    if request.user.is_authenticated:
        if request.user.cliente.carrito is not None:
            cartQty = request.user.cliente.carrito.cantidadTotal
        else:
            cartQty = 0
    elif request.user.is_anonymous:
            cartQty = 0
    products = Producto.objects.filter(mascota=2)
    template = loader.get_template("gallery.html")
    context = {"cart_cantidad": cartQty, "Productos": products, "titulo_galeria": "Perros", "jumbotron_titulo": "Productos para Perros", "jumbotron_subtitulo": "¡Todo para el mejor amigo del hombre!", "jumbotron_fondo": 'tienda/img/terrier.jpg'}
    return HttpResponse(template.render(context, request))

def contactMessages(request):
    mensajes = MensajesContacto.objects.all().values()
    context = {'Mensajes': mensajes}
    template = loader.get_template("messageList.html")
    return HttpResponse(template.render(context, request))

def removeMessage(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        mensaje = MensajesContacto.objects.get(pk=id)
        mensaje.delete()
        return redirect('/mensajes/')


def editUser(request):
    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(pk=request.user.id)
            cliente = Cliente.objects.get(pk=request.user.cliente.id)
            if request.user.email != request.POST['correo']:
                usuario.email = request.POST['correo']
            if request.user.cliente.primerNombre != request.POST['primer_nombre']:
                cliente.primerNombre = request.POST['primer_nombre']
            if request.user.cliente.segundoNombre != request.POST['segundo_nombre']:
                cliente.segundoNombre = request.POST['segundo_nombre']
            if request.user.cliente.primerApellido != request.POST['primer_apellido']:
                cliente.primerApellido = request.POST['primer_apellido']
            if request.user.cliente.segundoApellido != request.POST['segundo_apellido']:
                cliente.segundoApellido = request.POST['segundo_apellido']
            if request.user.cliente.direccion != request.POST['direccion']:
                cliente.direccion = request.POST['direccion']
            if request.user.cliente.comuna_id != request.POST['comuna']:
                cliente.comuna_id = request.POST['comuna']
            usuario.save() 
            cliente.save()
            return JsonResponse({'stuatus':'Actualización realizada'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
    else:
        template = loader.get_template("editInfo.html")
        comunas = Comuna.objects.all().values()
        context = {'Comunas': comunas}
        return HttpResponse(template.render(context, request))

def changePass(request):
    if request.method == 'POST':
        old_password = request.POST['oldpassword']
        new_password = request.POST['newpassword']
        usuario = request.user
        current_password = request.POST['oldpassword']
        usuario = authenticate(email=usuario.email, password=old_password)
        if usuario is None:
            return JsonResponse({'message': 'invalid_pass'})
        else:
            matchpass = check_password(old_password, new_password)
            if matchpass:
                return JsonResponse({'message': 'same_pass'}, status=200)
            else:
                usuario.set_password(new_password)
                usuario.save()
                update_session_auth_hash(request, usuario)
                return JsonResponse({'message': 'ok'}, status=200)
        

def registroForm(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['rut']
            resultant = rut.split('-')
            primer_nombre = form.cleaned_data['primer_nombre']
            segundo_nombre = form.cleaned_data['segundo_nombre']
            primer_apellido = form.cleaned_data['primer_apellido']
            segundo_apellido = form.cleaned_data['segundo_apellido']
            direccion = form.cleaned_data['direccion']
            cliente = Cliente.objects.create(rut=int(resultant[0]), dv=resultant[1], primerNombre=primer_nombre, segundoNombre=segundo_nombre, primerApellido=primer_apellido, segundoApellido=segundo_apellido, direccion=direccion, comuna_id=308)
            cliente.save()
            password = form.cleaned_data['password']
            correo = form.cleaned_data['correo']
            usuario = Usuario()
            usuario.set_password(password)
            usuario.email = correo
            usuario.cliente = cliente
            usuario.save()
            return redirect('/')
    else:
        form = RegistroForm()
        #regiones = Region.objects.all().values() #para resolver una escoba que tengo en la DB 
        regiones = Comuna.objects.all().values()
    return render(request, 'signup.html', {'form': form, 'titulo_pagina': 'Registrarse', 'Regiones': regiones})

def checkout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            optradio = request.POST['optradio']
            titular = request.POST['titular']
            numero = request.POST['numero']
            fecha = request.POST['fecha']
            carrito = request.user.cliente.carrito
            detalle = DetalleCarrito.objects.filter(carrito=carrito)
            pago = Pago()
            pago.cliente = request.user.cliente
            pago.metodo_pago = optradio
            pago.titular = titular
            pago.numero_tarjeta = numero
            pago.fecha_tarjeta = fecha
            pago.monto = carrito.valorTotal
            pago.detalle = serializers.serialize('json', detalle)
            pago.save()
            carrito.cantidadTotal = 0
            carrito.valorTotal = 0
            carrito.save()
            detalle.delete()
        return JsonResponse({'status': 'Compra efectuada!'}, status=200)
    else:
        if request.user.is_authenticated:
            carrito = request.user.cliente.carrito
            detalles = DetalleCarrito.objects.filter(carrito=carrito)
            if detalles.exists():
                detalles = DetalleCarrito.objects.all().select_related('producto')
                comuna = Comuna.objects.get(pk=request.user.cliente.comuna.id)
                provincia = Provincia.objects.get(pk=comuna.provincia.id)
                region = Region.objects.get(pk=provincia.region.id)
                context = {"Detalles": detalles, "Carrito":carrito, 'Region': region, 'Comuna':comuna}
                return render(request, 'checkout.html', context)
            else:
                return redirect('/')

def addToCarritoAction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        cantidad = int(data.get('cantidad', 1))
        if request.user.is_authenticated:
            try:
                producto = Producto.objects.get(pk=producto_id)
                producto.conteoVistas += 1
                producto.save()
                carrito = request.user.cliente.carrito
                detalle, created = DetalleCarrito.objects.get_or_create(producto=producto, carrito=carrito, defaults={'cantidad': 0, 'precioTotal': 0})
                detalle.cantidad += cantidad
                detalle.precioTotal += producto.precio * cantidad
                detalle.save()
                carrito.cantidadTotal += detalle.cantidad
                carrito.valorTotal += detalle.precioTotal   
                carrito.save()
                return JsonResponse({'status': 'Producto añadido'}, status=200)
            except Producto.DoesNotExist:
                return JsonResponse({'status': 'failure', 'error': 'Producto no existe'}, status=400)
            except Carrito.DoesNotExist:
                return JsonResponse({'status': 'failure', 'error': 'Carrito no existe'}, status=400)
            except ValueError:
                return JsonResponse({'status': 'failure', 'error': 'cantidad should be an integer'}, status=400)
            except Exception as e:
                return JsonResponse({'status': 'failure', 'error': str(e)}, status=400)
        else:
            return HttpResponse('Petición HTTP no válida para este método', status=405)



def removeSameRowAction(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        if request.user.is_authenticated:
            try:
                carrito = request.user.cliente.carrito
                producto = Producto.objects.get(pk=producto_id)
                detalle_carrito = DetalleCarrito.objects.get(carrito=carrito, producto=producto)
                precio_a_descontar = detalle_carrito.precioTotal
                cantidad_a_descontar = detalle_carrito.cantidad
                carrito.cantidadTotal -= cantidad_a_descontar
                carrito.valorTotal -= precio_a_descontar
                detalle_carrito.delete()
                carrito.save()
                context = {'valor_total': carrito.valorTotal}
                return JsonResponse({'status': 'success', 'message': 'Productos removidos del carrito exitosamente', 'context': context}, status=200)
            except Carrito.DoesNotExist:
                return JsonResponse({'status': 'failure', 'error': 'El carrito no existe'}, status=400)
            except Producto.DoesNotExist:
                return JsonResponse({'status': 'failure', 'error': 'El producto no existe'}, status=400)
            except DetalleCarrito.DoesNotExist:
                return JsonResponse({'status': 'failure', 'error': 'El producto no está en el carro'}, status=400)
            except Exception as e:
                return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
        else:
            return JsonResponse({'status': 'failure', 'error': 'Petición HTTP inválida'}, status=405)



def updateCartAction(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        cantidad = int(data.get('cantidad_producto'))

        if request.user.is_authenticated:
            try:
                producto = Producto.objects.get(pk=producto_id)
                carrito = request.user.cliente.carrito
                detalle = DetalleCarrito.objects.get(producto=producto, carrito=carrito)
                detalle.precioTotal = producto.precio * cantidad
                detalle.cantidad = cantidad

                if detalle.cantidad <= 0:
                    detalle.delete()
                else:
                    detalle.save()
                
                total_cantidad = DetalleCarrito.objects.filter(carrito=carrito).aggregate(Sum('cantidad'))['cantidad__sum']
                total_precio = DetalleCarrito.objects.filter(carrito=carrito).aggregate(Sum('precioTotal'))['precioTotal__sum']

                if total_cantidad and total_precio is None:
                    total_cantidad = 0
                    total_precio = 0
                carrito.cantidadTotal = total_cantidad
                carrito.valorTotal = total_precio
                carrito.save()

                context = {'precio_total': detalle.precioTotal, 'valor_total': carrito.valorTotal}
                return JsonResponse({'status': 'success', 'message':'Producto actualizado', 'context': context}, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'failure', 'error': 'Producto, Carrito, or DetalleCarrito does not exist', 'context': context}, status=400)
            except Exception as e:
                return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'failure', 'error': 'Invalid request method'}, status=405)


def getCartDetails(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            try:
                carrito = request.user.cliente.carrito
                detalles = DetalleCarrito.objects.filter(carrito=carrito).select_related('producto')

                detalles_list = []
                for detalle in detalles:
                    detalle_dict = {
                        'id': detalle.producto.id,
                        'nombre': detalle.producto.nombre,
                        'cantidad': detalle.cantidad,
                        'precio_unitario': detalle.producto.precio,
                        'precio_total': detalle.precioTotal,
                        'imagen': detalle.producto.imagen
                    }
                    detalles_list.append(detalle_dict)

                return JsonResponse({'status': 'success', 'detalles': detalles_list})
            except Carrito.DoesNotExist:
                return JsonResponse({'status': 'failure', 'error': 'El carrito solicitado no existe'}, status=400)
            except Exception as e:
                return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'failure', 'error': 'Petición HTTP inválida'}, status=405)


def deleteAllCart(request):
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            try:
                carrito = request.user.cliente.carrito
                detalles = DetalleCarrito.objects.filter(carrito=carrito)
                detalles.delete()
                carrito.cantidadTotal = 0
                carrito.valorTotal = 0
                carrito.save()
                return JsonResponse({'status': 'success'}, status=200)
            except Carrito.DoesNotExist:
                return JsonResponse({'status': 'failure', 'error': 'El carrito solicitado no existe'}, status=400)
            except Exception as e:
                return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'failure', 'error': 'Petición HTTP inválida'}, status=405)

def modalCarro(request):
    if request.user.is_authenticated:
        try:
            carrito = request.user.cliente.carrito
            detalles = DetalleCarrito.objects.filter(carrito=carrito)
        except:
            carrito = None
            detalles = None
    context = {"Detalles": detalles, "Carrito": carrito}
    return render(request, "components/modals/modalCarrito.html", context)

def modalProducto(request, id): #Sé que lo ideal es que esta request sea por POST, pero quiero simplificarme la vida a estas alturas del año
    producto = Producto.objects.get(pk=id)
    producto.conteoVistas += 1
    producto.save()
    context = {"Producto": producto}
    return render(request, "components/modals/modalProducto.html", context)

def modalCUD(request):
    mascotas = Mascota.objects.values()
    categorias = Categoria.objects.values()
    context = {"Mascotas": mascotas, "Categorias": categorias}
    return render(request, "components/modals/modalCUD.html", context)

def reloadCartButtton(request):
    detalles = DetalleCarrito.objects.all().select_related('producto') #hardcodeado por ahora para mostrar todos los carros
    cartQty = 0
    for d in detalles:
        cartQty+= d.cantidad
    # context = {"carrito_numero": cartQty}
    # return render(request, "components/cartButton.html", context)
    html = render_to_string('components/cartButton.html', {"carrito_numero": cartQty})
    return HttpResponse(html)

def addProduct(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        precio = request.POST['precio']
        stock = request.POST['stock']
        descripcion =request.POST['descripcion']
        idMascota = request.POST['mascota']
        idCategoria = request.POST['categoria']
        imagen = request.FILES.get('imageUpload')
    
        #hack horrendo para guardar las imágenes en el directorio estático y luego servilas
        file_path = os.path.join('static/tienda/img', imagen.name)
        file_path = default_storage.get_available_name(file_path) 

        file = default_storage.save(file_path, ContentFile(imagen.read()))
        uploaded_file_url = default_storage.url(file)
        uploaded_file_url = uploaded_file_url.replace('/static/', '', 1)
        try:
            mascota = Mascota.objects.get(pk=idMascota)
            categoria = Categoria.objects.get(pk=idCategoria)
            Producto.objects.create(nombre=nombre, precio=precio, stock=stock, imagen=uploaded_file_url, mascota=mascota, categoria=categoria, descripcion=descripcion)
            return JsonResponse({'status': 'sucess', 'message': 'Producto creado correctamente.'})
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)

    else:
        return JsonResponse({'status': 'failure', 'error': 'Petición HTTP inválida'})

def removeProduct(request):
    if request.method == 'DELETE':
        if request.user.is_authenticated and request.user.is_staff == True:
            data = json.loads(request.body)
            producto_id = data.get('producto_id')
            try:
                producto = Producto.objects.get(pk=producto_id)
                producto.delete()
                return JsonResponse({'status': 'success'}, status=200)
            except Carrito.DoesNotExist:
                return JsonResponse({'status': 'failure', 'error': 'El producto solicitado no existe'}, status=400)
            except Exception as e:
                return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
        else:
            return JsonResponse({'status': 'failure', 'error':'No está autorizado para realizar esta operación'}, status=403)        
    else:
        return JsonResponse({'status': 'failure', 'error': 'Petición HTTP inválida'}, status=405)

def donarInForm(request):
    if request.method == 'POST':
        form = DonarForm(request.POST)
        errors = str(form.errors)
        if form.is_valid():
            donacion = Donante()
            pago = Pago()
            donacion.nombre = form.cleaned_data['nombre']
            donacion.primerApellido = form.cleaned_data['apellido']
            rut = form.cleaned_data['rut']
            resultant = rut.split('-')
            donacion.rut = int(resultant[0])
            donacion.dv = resultant[1]
            donacion.correo = form.cleaned_data['correo']
            donacion.telefono = form.cleaned_data['celular']
            donacion.save()
            pago.metodo_pago = form.cleaned_data['optradio']
            pago.titular = form.cleaned_data['titular']
            pago.numero_tarjeta = form.cleaned_data['numero']
            pago.fecha_tarjeta = form.cleaned_data['fecha']
            pago.monto = form.cleaned_data['cantidad']
            pago.donante = donacion
            pago.save()
            return JsonResponse({'status': 'sucess'}, status=200)
        else: 
            return JsonResponse({'status': 'failure', 'error':errors}, status=403)       
    else:
        form = DonarForm()
        return render(request, 'donacion.html', {'form': form})

def contactInForm(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        errors = str(form.errors)
        if form.is_valid():
            mensaje = MensajesContacto()
            mensaje.nombre = form.cleaned_data['nombre']
            mensaje.email = form.cleaned_data['email']
            mensaje.motivoContacto = form.cleaned_data['razon']
            mensaje.message = form.cleaned_data['comentario']
            mensaje.save()
            return JsonResponse({'status': 'sucess'}, status=200)
        else: 
            return JsonResponse({'status': 'failure', 'error':errors}, status=403)
    form = ContactoForm()
    if request.user.is_authenticated:
        if request.user.cliente.carrito is not None:
            cartQty = request.user.cliente.carrito.cantidadTotal
        else:
            cartQty = 0
    elif request.user.is_anonymous:
            cartQty = 0 
    template = loader.get_template("contacto.html") 
    context = {'form': form, "cart_cantidad": cartQty}
    #return render(request, 'contacto.html', context)
    return HttpResponse(template.render(context, request))        

def modalConfirmaBorradoProducto(request):
    context = {}
    return render(request, "components/modals/modalConfirm.html", context)

def modalLogin(request):
    context = {}
    return render(request, 'components/modals/modalLogin.html')

def modalUpdate(request, producto_id):
    producto = Producto.objects.get(pk=producto_id)
    mascota = producto.mascota
    categoria = producto.categoria
    mascotas = Mascota.objects.all()
    categorias = Categoria.objects.all()
    context = {"Producto":producto, "Mascotas": mascotas, "Categorias": categorias}
    return render(request, "components/modals/modalCUD.html", context)

def modalDonacion(request):
    context = {}
    return render(request, 'components/modals/modalDonacion.html')


def modalErrores(request):
    data = json.loads(request.body)
    titulo = data.get('titulo_modal')
    mensaje = data.get('mensaje_modal')
    context = {'modal_titulo': titulo, 'modal_mensaje': mensaje}
    return render(request, 'components/modals/modalErrores.html', context)

def modalCambioPass(request):
    context = {}
    return render(request,'components/modals/modalChangePass.html', context)

def updateProduct(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_staff == True:
            producto_id = request.POST['producto_id']
            nombre = request.POST['nombre']
            precio = request.POST['precio']
            stock = request.POST['stock']
            descripcion = request.POST['descripcion']
            idMascota = request.POST['mascota']
            idCategoria = request.POST['categoria']
            if 'imageUpload' in request.FILES:
                imagen = request.FILES.get('imageUpload')
                #hack horrendo para guardar las imágenes en el directorio estático y luego servirlas
                file_path = os.path.join('static/tienda/img', imagen.name)
                file_path = default_storage.get_available_name(file_path) 
                file = default_storage.save(file_path, ContentFile(imagen.read()))
                uploaded_file_url = default_storage.url(file)
                uploaded_file_url = uploaded_file_url.replace('/static/', '', 1)
            else: 
                imagen = None
            productoUpdate = Producto.objects.get(pk=producto_id)
            mascotaUpdate = Mascota.objects.get(pk=idMascota)
            categoriaUpdate= Categoria.objects.get(pk=idCategoria)
            try:
                productoUpdate.nombre = nombre
                productoUpdate.precio = precio
                productoUpdate.stock = stock
                productoUpdate.mascota = mascotaUpdate
                productoUpdate.descripcion = descripcion
                if imagen != None:
                    productoUpdate.imagen = uploaded_file_url
                productoUpdate.save()
                return JsonResponse({'status': 'success', 'message': 'Producto actualizado exitosamente'}, status=200)
            except Exception as e:
                return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
        else:
            return JsonResponse({'status': 'failure', 'error': 'Usuario no autorizado para ejecutar esta acción.'}, status=403)
    else:
        return JsonResponse({'status': 'failure', 'error': 'Petición HTTP inválida'}, status=405)

def cartStats(request):
    if request.user.is_authenticated:
        carrito = request.user.cliente.carrito
        detalles = list(DetalleCarrito.objects.filter(carrito=carrito).values())
    return JsonResponse({"valor_total": carrito.valorTotal, "detalles": detalles })

def comunasFromRegion(request, id):
    comunas = Comuna.objects.filter(provincia__region__id=id)
    datos = [{'id': comuna.id, 'nombre': comuna.nombre} for comuna in comunas]
    return JsonResponse(datos, safe=False)