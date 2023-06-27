from tienda import views
from django.conf import settings
from django.conf.urls.static import static
"""
URL configuration for tiendaPET project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('gatos/', views.cats),
    path('perros/', views.dogs),
    path('contacto/', views.contact),
    #Paths que implementan API
    path('api/addItem', views.addToCarritoAction),
    path('api/removeAllTheSameItems/<int:carrito_id>/<int:producto_id>/', views.removeSameRowAction),
    path('api/updateItems', views.updateCartAction),
    path('api/getItems/<int:carrito_id>', views.getCartDetails),
    path('api/getModalCart/', views.modalCarro),
    path('api/getModalProducto/<int:id>', views.modalProducto),
    path('api/cartButtonUpdate', views.reloadCartButtton), 
    path('api/deleteEntireCart/<int:carrito_id>', views.deleteAllCart)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

