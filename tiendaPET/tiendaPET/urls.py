from tienda import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
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
    path('', views.index, name='index'),
    path('gatos/', views.cats, name='gatos'),
    path('perros/', views.dogs, name='perros'),
    path('contacto/', views.contactInForm, name='contacto'),
    path('donar/', views.donarInForm, name='donar'),
    path('checkout/', views.checkout),
    #Paths que implementan API/AJAX
    path('ajax/addItem', views.addToCarritoAction),
    path('ajax/getModalLogin/', views.modalLogin),
    path('ajax/login/', views.login),
    path('ajax/removeAllTheSameItems/', views.removeSameRowAction),
    path('ajax/updateItems', views.updateCartAction),
    path('ajax/getItems/', views.getCartDetails),
    path('ajax/getModalCart/', views.modalCarro),
    path('ajax/getModalProducto/<int:id>', views.modalProducto),
    path('ajax/cartButtonUpdate', views.reloadCartButtton), 
    path('ajax/deleteEntireCart/', views.deleteAllCart),
    path('ajax/removeProduct/<int:producto_id>', views.removeProduct),
    path('ajax/addProduct', views.addProduct),
    path('ajax/getModalCUD', views.modalCUD),
    path('ajax/getModalUpdate/<int:producto_id>', views.modalUpdate),
    path('ajax/updateProduct/<int:producto_id>', views.updateProduct),
    path('ajax/getModalConfirm', views.modalConfirmaBorradoProducto),
    path('ajax/getCartStats', views.cartStats)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

