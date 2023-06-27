from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils.html import mark_safe
from .models import Productos, DetalleCarrito, Carrito
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.template.loader import render_to_string
# Create your views here.

def index(request):
    detalles = DetalleCarrito.objects.all().select_related('producto') #hardcodeado por ahora para mostrar todos los carros
    cartQty = 0
    for d in detalles:
        cartQty+= d.cantidad
    products = Productos.objects.order_by('-conteoVistas')[:6]
    context = {"cart_cantidad": cartQty,"jumbotron_titulo": "Somos TiendaPET", "jumbotron_subtitulo": "Tenemos los mejores productos para tu mascota", "jumbotron_fondo": 'tienda/img/boxer.jpg', "jumbotron_opt": mark_safe('<button class="btn btn-primary btn-lg" type="button" data-bs-toggle="modal" data-bs-target="#modalNosotros">Sobre Nosotros</button>')}
    for i in range(6):
        context['producto{}_id'.format(i+1)] = products[i].id
        context['producto{}_nombre'.format(i+1)] = products[i].nombre
        context['producto{}_precio'.format(i+1)] = products[i].precio
        context['producto{}_imagen'.format(i+1)] = products[i].imagen
    template = loader.get_template("index.html")
    return HttpResponse(template.render(context,request))

def cats(request):
    products = Productos.objects.filter(mascota=1)
    detalles = DetalleCarrito.objects.all().select_related('producto') #hardcodeado por ahora para mostrar todos los carros
    cartQty = 0
    for d in detalles:
        cartQty+= d.cantidad
    template = loader.get_template("gallery.html")
    context = {"cart_cantidad": cartQty, "Productos": products, "titulo_galeria": "Gatos", "jumbotron_titulo": "Productos para Gatos", "jumbotron_subtitulo": "¡Todo para los reyes del hogar!", "jumbotron_fondo": 'tienda/img/kitten.jpg'}
    return HttpResponse(template.render(context, request))

def dogs(request):
    products = Productos.objects.filter(mascota=2)
    detalles = DetalleCarrito.objects.all().select_related('producto')
    cartQty = 0
    for d in detalles:
        cartQty+= d.cantidad
    template = loader.get_template("gallery.html")
    context = {"cart_cantidad": cartQty, "Productos": products, "titulo_galeria": "Perros", "jumbotron_titulo": "Productos para Perros", "jumbotron_subtitulo": "¡Todo para el mejor amigo del hombre!", "jumbotron_fondo": 'tienda/img/terrier.jpg'}
    return HttpResponse(template.render(context, request))

def contact(request):
    detalles = DetalleCarrito.objects.all().select_related('producto')
    cartQty = 0
    for d in detalles:
        cartQty+= d.cantidad
    template = loader.get_template("contacto.html")
    context = {"cart_cantidad": cartQty}
    return HttpResponse(template.render(context, request))

def addProductToCart(producto, carrito, cantidad):
    detalle, created = DetalleCarrito.objects.get_or_create(producto=producto, carrito=carrito, defaults={'cantidad': 0, 'precioTotal': 0})
    detalle.cantidad += cantidad
    detalle.precioTotal += producto.precio * cantidad
    detalle.save()
    carrito.valorTotal += producto.precio * cantidad
    carrito.save()

@csrf_exempt
def addToCarritoAction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        carrito_id = data.get('carrito_id')
        cliente_id = data.get('cliente_id')
        cantidad = int(data.get('cantidad', 1))

        try:
            producto = Productos.objects.get(pk=producto_id)
            if cliente_id == 0:
                carrito, created = Carrito.objects.get_or_create(pk=carrito_id, defaults={'valorTotal': 0})
            else:
                cliente= Clientes.objects.get(pk=id)
                carrito, created = Carrito.objects.get_or_create(cliente=cliente, defaults={'valorTotal': 0})
            addProductToCart(producto, carrito, cantidad)
            return JsonResponse({'status': 'Producto añadido'}, status=200)
        except Productos.DoesNotExist:
            return JsonResponse({'status': 'failure', 'error': 'Producto no existe'}, status=400)
        except Carrito.DoesNotExist:
            return JsonResponse({'status': 'failure', 'error': 'Carrito no existe'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=400)
    else:
        return HttpResponse('Invalid request method', status=405)

@csrf_exempt
def removeSameRowAction(request, carrito_id, producto_id): #borra los mismos tipos de productos del carrito
    if request.method == 'GET':
        try:
            carrito = Carrito.objects.get(pk=carrito_id)
            producto = Productos.objects.get(pk=producto_id)
            detalle_carrito = DetalleCarrito.objects.get(carrito=carrito, producto=producto)
            detalle_carrito.delete()

            return JsonResponse({'status': 'success', 'message': 'Productos removidos del carrito'})
        except Carrito.DoesNotExist:
            return JsonResponse({'status': 'failure', 'error': 'El carrito no existe'}, status=400)
        except Productos.DoesNotExist:
            return JsonResponse({'status': 'failure', 'error': 'El producto no existe'}, status=400)
        except DetalleCarrito.DoesNotExist:
            return JsonResponse({'status': 'failure', 'error': 'El producto no está en el carro'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'failure', 'error': 'Petición HTTP inválida'}, status=405)


@csrf_exempt
def updateCartAction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        carrito_id = data.get('carrito_id')
        cantidad = int(data.get('cantidad_producto'))

        try:
            # Find the product and cart
            producto = Productos.objects.get(pk=producto_id)
            carrito = Carrito.objects.get(pk=carrito_id)

            # Get the detail cart record
            detalle = DetalleCarrito.objects.get(producto=producto, carrito=carrito)
            
            # Update the total price and quantity in the detail cart
            carrito.valorTotal -= detalle.precioTotal
            detalle.precioTotal = producto.precio * cantidad
            detalle.cantidad = cantidad

            if detalle.cantidad <= 0:
                # If quantity is 0 or less, delete the detail cart record
                detalle.delete()
            else:
                detalle.save()
                carrito.valorTotal += detalle.precioTotal

            # If no more detail cart records for the cart, delete the cart
            if not DetalleCarrito.objects.filter(carrito=carrito).exists():
                carrito.delete()
            else:
                carrito.save()

            return JsonResponse({'status': 'success'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'failure', 'error': 'Producto, Carrito, or DetalleCarrito does not exist'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'failure', 'error': 'Invalid request method'}, status=405)
@csrf_exempt
def getCartDetails(request, carrito_id):
    if request.method == 'GET':
        try:
            carrito = Carrito.objects.get(pk=carrito_id)
            detalles = DetalleCarrito.objects.filter(carrito=carrito).select_related('producto')

            # Manually serializing to JSON
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
def deleteAllCart(request, carrito_id):
    if request.method == 'GET':
        try:
            carrito = Carrito.objects.get(pk=carrito_id)
            detalles = DetalleCarrito.objects.filter(carrito=carrito)
            detalles.delete()
            carrito.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Carrito.DoesNotExist:
            return JsonResponse({'status': 'failure', 'error': 'El carrito solicitado no existe'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'failure', 'error': 'Petición HTTP inválida'}, status=405)
def modalCarro(request):
    detalles = DetalleCarrito.objects.all().select_related('producto')
    context = {"Detalles": detalles}
    return render(request, "components/modals/modalCarrito.html", context)

def modalProducto(request, id):
    producto = Productos.objects.get(pk=id)
    context = {"Producto": producto}
    return render(request, "components/modals/modalProducto.html", context)

def reloadCartButtton(request):
    detalles = DetalleCarrito.objects.all().select_related('producto') #hardcodeado por ahora para mostrar todos los carros
    cartQty = 0
    for d in detalles:
        cartQty+= d.cantidad
    # context = {"carrito_numero": cartQty}
    # return render(request, "components/cartButton.html", context)
    html = render_to_string('components/cartButton.html', {"carrito_numero": cartQty})
    return HttpResponse(html)