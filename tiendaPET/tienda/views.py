from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils.html import mark_safe
from .models import Producto, DetalleCarrito, Carrito, Mascota, Categoria
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.template.loader import render_to_string
from .forms import DonarForm, ContactoForm, AutenticacionForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.db.models import Sum

# Create your views here.


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'status':'success'}, status=200)
        else:
            return JsonResponse({'status':'invalid'}, status=400)

def index(request):
    if request.user.is_authenticated or request.user.is_anonymous:
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
    if request.user.is_authenticated or request.user.is_anonymous:
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
    if request.user.is_authenticated or request.user.is_anonymous:
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

def checkout(request):
    if request.user.is_authenticated:
        carrito = request.user.cliente.carrito
        detalles = DetalleCarrito.objects.filter(carrito=carrito)
        if detalles.exists():
            detalles = DetalleCarrito.objects.all().select_related('producto')
            context = {"Detalles": detalles, "Carrito":carrito}
            return render(request, 'checkout.html', context)
        else:
            return redirect('/')
@csrf_exempt
def contactInForm(request):
    form = ContactoForm()
    if request.user.is_authenticated or request.user.is_anonymous:
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

def addProductToCart(producto, carrito, cantidad):
    detalle, created = DetalleCarrito.objects.get_or_create(producto=producto, carrito=carrito, defaults={'cantidad': 0, 'precioTotal': 0})
    detalle.cantidad += cantidad
    detalle.precioTotal += producto.precio * cantidad
    detalle.save()
    carrito.valorTotal += producto.precio * cantidad
    carrito.save()

@csrf_exempt
# def addToCarritoAction(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         producto_id = data.get('producto_id')
#         carrito_id = data.get('carrito_id')
#         cliente_id = data.get('cliente_id')
#         cantidad = int(data.get('cantidad', 1))

#         try:
#             producto = Producto.objects.get(pk=producto_id)
#             if cliente_id == 0:
#                 carrito, created = Carrito.objects.get_or_create(pk=carrito_id, defaults={'valorTotal': 0})
#             else:
#                 cliente= Clientes.objects.get(pk=id)
#                 carrito, created = Carrito.objects.get_or_create(cliente=cliente, defaults={'valorTotal': 0})
#             addProductToCart(producto, carrito, cantidad)
#             return JsonResponse({'status': 'Producto añadido'}, status=200)
#         except Producto.DoesNotExist:
#             return JsonResponse({'status': 'failure', 'error': 'Producto no existe'}, status=400)
#         except Carrito.DoesNotExist:
#             return JsonResponse({'status': 'failure', 'error': 'Carrito no existe'}, status=400)
#         except Exception as e:
#             return JsonResponse({'status': 'failure', 'error': str(e)}, status=400)
#     else:
#         return HttpResponse('Invalid request method', status=405)
def addToCarritoAction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        cantidad = int(data.get('cantidad', 1))
        if request.user.is_authenticated:
            try:
                producto = Producto.objects.get(pk=producto_id)
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
            return HttpResponse('Método de petición no válido para este método', status=405)


@csrf_exempt
# def removeSameRowAction(request, carrito_id, producto_id): #borra los mismos tipos de productos del carrito
#     if request.method == 'GET':
#         try:
#             carrito = Carrito.objects.get(pk=carrito_id)
#             producto = Producto.objects.get(pk=producto_id)
#             detalle_carrito = DetalleCarrito.objects.get(carrito=carrito, producto=producto)
#             detalle_carrito.delete()

#             return JsonResponse({'status': 'success', 'message': 'Productos removidos del carrito'})
#         except Carrito.DoesNotExist:
#             return JsonResponse({'status': 'failure', 'error': 'El carrito no existe'}, status=400)
#         except Producto.DoesNotExist:
#             return JsonResponse({'status': 'failure', 'error': 'El producto no existe'}, status=400)
#         except DetalleCarrito.DoesNotExist:
#             return JsonResponse({'status': 'failure', 'error': 'El producto no está en el carro'}, status=400)
#         except Exception as e:
#             return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'status': 'failure', 'error': 'Petición HTTP inválida'}, status=405)

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



# @csrf_exempt
# def updateCartAction(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         producto_id = data.get('producto_id')
#         carrito_id = data.get('carrito_id')
#         cantidad = int(data.get('cantidad_producto'))

#         try:
#             # Find the product and cart
#             producto = Producto.objects.get(pk=producto_id)
#             carrito = Carrito.objects.get(pk=carrito_id)

#             # Get the detail cart record
#             detalle = DetalleCarrito.objects.get(producto=producto, carrito=carrito)
            
#             # Update the total price and quantity in the detail cart
#             carrito.valorTotal -= detalle.precioTotal
#             detalle.precioTotal = producto.precio * cantidad
#             detalle.cantidad = cantidad

#             if detalle.cantidad <= 0:
#                 # If quantity is 0 or less, delete the detail cart record
#                 detalle.delete()
#             else:
#                 detalle.save()
#                 carrito.valorTotal += detalle.precioTotal

#             # If no more detail cart records for the cart, delete the cart
#             if not DetalleCarrito.objects.filter(carrito=carrito).exists():
#                 carrito.delete()
#             else:
#                 carrito.save()

#             return JsonResponse({'status': 'success'}, status=200)
#         except ObjectDoesNotExist:
#             return JsonResponse({'status': 'failure', 'error': 'Producto, Carrito, or DetalleCarrito does not exist'}, status=400)
#         except Exception as e:
#             return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'status': 'failure', 'error': 'Invalid request method'}, status=405)

@csrf_exempt
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



@csrf_exempt
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

@csrf_exempt
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
    id_cart = 0
    if request.user.is_authenticated and request.user.is_staff == False:
        if request.user.cliente.carrito is not None:
            id_cart = request.user.cliente.carrito.id
    try:
        carrito = Carrito.objects.get(pk=id_cart) #hardcodeado por ahora
        detalles = DetalleCarrito.objects.filter(carrito__id=id_cart)
    except:
        carrito = None
        detalles = None
    context = {"Detalles": detalles, "Carrito": carrito}
    return render(request, "components/modals/modalCarrito.html", context)

def modalProducto(request, id):
    producto = Producto.objects.get(pk=id)
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

# def reloadCartButtton(request):
#     if request.user.is_authenticated and request.user.is_staff == False:
#         if request.user.cliente.carrito is None:
#             cartQty = 0
#         else:
#             cartQty = request.user.cliente.carrito.cantidadTotal

@csrf_exempt
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
            Producto.objects.create(nombre=nombre, precio=precio, stock=stock, imagen=uploaded_file_url, mascota=mascota, categoria=categoria)
            return JsonResponse({'status': 'sucess', 'message': 'Producto creado correctamente.'})
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)

    else:
        return JsonResponse({'status': 'failure', 'error': 'Petición HTTP inválida'})

def removeProduct(request, producto_id):
    if request.method == 'GET':
        try:
            producto = Producto.objects.get(pk=producto_id)
            producto.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Carrito.DoesNotExist:
            return JsonResponse({'status': 'failure', 'error': 'El producto solicitado no existe'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'failure', 'error': 'Petición HTTP inválida'}, status=405)

def donar(request):
    context = {}
    return render(request, 'donacionStatic.html', context)

def donarInForm(request):
    if request.method == 'POST':
        form = DonarForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario aquí
            cantidad = form.cleaned_data['cantidad']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            rut = form.cleaned_data['rut']
            correo = form.cleaned_data['correo']
            celular = form.cleaned_data['celular']
            metodo_pago = form.cleaned_data['optradio']
            titular = form.cleaned_data['titular']
            numero = form.cleaned_data['numero']
            codigo = form.cleaned_data['codigo']
            fecha = form.cleaned_data['fecha']
            return redirect('index.html')  # Reemplaza 'index' con la URL correspondiente a tu página de éxito

    else:
        form = DonarForm()

    return render(request, 'donacion.html', {'form': form})

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
@csrf_exempt
def updateProduct(request, producto_id):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        precio = request.POST['precio']
        stock = request.POST['stock']
        descripcion = request.POST['descripcion']
        idMascota = request.POST['mascota']
        idCategoria = request.POST['categoria']
        if 'imageUpload' in request.FILES:
            imagen = request.FILES.get('imageUpload')
            #hack horrendo para guardar las imágenes en el directorio estático y luego servilas
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
            if imagen != None:
                productoUpdate.imagen = uploaded_file_url
            productoUpdate.save()
            return JsonResponse({'status': 'success', 'message': 'Producto actualizado exitosamente'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'failure', 'error': 'Petición HTTP inválida'}, status=405)

def cartStats(request):
    carrito = Carrito.objects.get(pk=1)
    detalles = list(DetalleCarrito.objects.filter(carrito=carrito).values())

    return JsonResponse({"valor_total": carrito.valorTotal, "detalles": detalles })