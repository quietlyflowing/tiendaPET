$(document).ready(function() {
BASE_URL = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port;
console.log('App V2. Ready!')
//Añade un listener al botón del carrito para invocar el modal de bootstrap desde Django
 $('#botonCarro').click(function() {
    $.get(BASE_URL+'/api/getModalCart', function(data) {
        $(data).appendTo('#tiendaNav');
        //Acá procedemos a añadir los listeners para el detalle del carro de compras
        //Botón 1: Vacía todo el carro de compras:
        $('#killCarroStorage').click(function() {
            $.get(BASE_URL+'/api/deleteEntireCart/1', function() {
                console.log(data)
            }); //hardcodeado por mientras
        });
        //Boton 2: Se va a la página de pago.
        $('#buttonCheckoOut').click(function(){
            console.log("Te estoy redireccionando a la página de pago!")
        });
        //Botón 3: Elmina la fila de la página de pago
        $("td > .btn.btn-danger").click(function() {
            
            var carrito_id = 1 //hardcodeado por ahora
            var id_string = $(this).attr('id');
            var arrayString = id_string.split('_');
             $.get(BASE_URL+'/api/removeAllTheSameItems/'+carrito_id + '/' +arrayString[1]+ '/', function(data){
                 console.log(data)
                 $('#'+id_string).closest('tr').remove();
             });
        });
        $("td > .form-control").change(function() {
            var cantidad = $(this).val();
            var id_string = $(this).attr('id');
            var arrayString = id_string.split('_');
            console.log(arrayString);
            console.log(cantidad);
            var datos = {producto_id: arrayString[1], carrito_id: 1, cantidad_producto: cantidad};
            $.post(BASE_URL+'/api/updateItems', JSON.stringify(datos), function(response){console.log(response)});
        });        
         $('#modalCarrito').modal('show');
         $('#modalCarrito').on('hidden.bs.modal', function (e) {
            $(this).remove();
            $.get(BASE_URL+'/api/cartButtonUpdate', function(data){ 
                console.log('Actualización del botón solicitada');
                $('#indicadorCarrito').html(data);
            });
        }); 
    });
 });
//Fin del procedimiento que añade los listeners 
//Procedimiento que añade listeners a las cards.
$("button").each(function() {
    if($(this).parent().hasClass('card-body') && $(this).hasClass('btn-primary')) {
        $(this).click(function() {
            const grandParent = $(this).parent().parent().attr('id');
            var datos = {producto_id: grandParent, carrito_id: 1, cantidad:1, cliente_id: 0}; //hardcodeado por ahora
            $.post(BASE_URL+'/api/addItem', JSON.stringify(datos), function(response) {
                console.log(response);
            }).done(function(){  $.get(BASE_URL+'/api/cartButtonUpdate', function(data){ 
                console.log('Actualización del botón solicitada');
                $('#indicadorCarrito').html(data);
            });
        });
        });
    }
});
//Fin del procedimiento que añade listeners a las cards.

//Procedimiento que crea listeners en los botones ver
$("button").each(function(){
    if($(this).parent().hasClass('card-body') && $(this).attr('id')==='botonVer') {
        $(this).click(function() {
            const grandParent = $(this).parent().parent().attr('id');
            $.get(BASE_URL+'/api/getModalProducto/'+grandParent, function(data){
                $(data).appendTo('#tiendaNav');
                $('#modalProducto').modal('show');
                $('#anadeProducto').click(function() {
                    var datos = {producto_id: grandParent, carrito_id: 1, cantidad:1, cliente_id: 0};
                    $.post(BASE_URL+'/api/addItem', JSON.stringify(datos), function(response) {
                        console.log(response);
                    }).done(function(){  $.get(BASE_URL+'/api/cartButtonUpdate', function(data){ 
                        console.log('Actualización del botón solicitada');
                        $('#indicadorCarrito').html(data);
                    });
                });
                });
                $('#modalProducto').on('hidden.bs.modal', function (e) {
                   $(this).remove();
               }); 
                console.log('Solicitando modal para producto con la PK nro ' + grandParent);
            });
        });
    }
});

});

// $.get('/api/getModalProducto/5', function(data) {
//     $(data).appendTo('#tiendaNav');
//      $('#modalProducto').modal('show'); 
// });