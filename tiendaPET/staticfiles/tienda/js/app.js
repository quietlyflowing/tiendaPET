$(document).ready(function() {
BASE_URL = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port;
console.log('App V2. Ready!')




//Procedimiento que añade listeners al modal de carrito.
$('.container').on('click', '#botonCarro', function() {
    console.log('Abriendo modal');
    $.get(BASE_URL+'/api/getModalCart/', function(data) {
        $(data).appendTo('#tiendaNav');
        $('#modalCarrito').modal('show');
        $('#modalCarrito').on('hidden.bs.modal', function(e) {
            $(this).remove();
            $.get(BASE_URL + '/api/cartButtonUpdate', function(data) {
                console.log('Actualización del botón solicitada');
                $('#indicadorCarrito').html(data);});});

        $('#buttonCheckoOut').click(function(){
            console.log("Te estoy redireccionando a la página de pago!")});
              //Botón 3: Elmina la fila de la página de pago
              $("td > .btn.btn-danger").click(function() {
                var carrito_id = 1 //hardcodeado por ahora
                var id_string = $(this).attr('id');
                var arrayString = id_string.split('_');
                 $.get(BASE_URL+'/api/removeAllTheSameItems/'+carrito_id + '/' +arrayString[1]+ '/', function(data){
                     console.log(data)
                     $('#'+id_string).closest('tr').remove();
                     if ($('#cuerpoTabla').children('tr').length === 0) {
                        $('.table').remove();
                        console.log('La tabla está vacía. Cerrando');
                        $('#modalCarrito').modal('hide');
                    }
                     $.get(BASE_URL + '/api/cartButtonUpdate', function(data) {
                        console.log('Actualización del botón solicitada');
                        $('#indicadorCarrito').html(data);
                    });
                 });
            });
            //Fin listener botón 3
            //Botón 4: // Actualiza el carrito conforme se mueve las cantidades 
            $("td > .form-control").change(function() {
                var cantidad = $(this).val();
                var id_string = $(this).attr('id');
                var arrayString = id_string.split('_');
                console.log(arrayString);
                console.log(cantidad);
                var datos = {
                    producto_id: arrayString[1],
                    carrito_id: 1,
                    cantidad_producto: cantidad
                };
                $.post(BASE_URL + '/api/updateItems', JSON.stringify(datos), function() {
                    $.get(BASE_URL + '/api/cartButtonUpdate', function(data) {
                        console.log('Actualización del botón solicitada');
                        $('#indicadorCarrito').html(data);
                    });
                });
            });
            //Fin Botón 4:
            //Botón 5: Elimina el carrito y cierra el modal.
            $('#killCarroStorage').on('click', function() {
                $.get(BASE_URL+'/api/deleteEntireCart/1', function() {
                    console.log(data)
                    $('.table').remove();
                    $('#modalCarrito').modal('hide');
                    $.get(BASE_URL + '/api/cartButtonUpdate', function(data) {
                        console.log('Actualización del botón solicitada');
                        $('#indicadorCarrito').html(data);
                    });
                });
            });
    });
});
//Fin del procedimiento que añade los listeners al modal

//Procedimiento que añade listeners al botón Agregar al Carro de las cards.
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
//Procedimiento que añade listeners al botón Eliminar de las cards
$("button").each(function(){
    if($(this).parent().hasClass('card-body') && $(this).text() === 'Eliminar') {
        $(this).click(function(){
            console.log('Soy un botón para eliminar productos');
        });
    }});
//fin procedimiento que añade listeners al botón Eliminar
//
$("button").each(function(){
    if($(this).parent().hasClass('card-body') && $(this).text() === 'Editar') {
        $(this).click(function(){
            console.log('Soy un botón para editar los productos');
        });
    }});
//Procedimiento que añade listeners al botón editar 

//Procedimiento que crea listeners en los botones ver
$("button").each(function(){
    if($(this).parent().hasClass('card-body') && $(this).text() === 'Ver') {
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

//Procedimiento para crear listener en el botón añadir
$('#botonCrud').on('click', function() {
    console.log('Soy un botón para añadir productos');
    $.get(BASE_URL + '/api/getModalCUD', function(data) {
        console.log('Abriendo modal CUD');
        $(data).appendTo('#tiendaNav');
        $('#modalCUD').modal('show');
        $('#modalCUD').on('hidden.bs.modal', function(e) {
            $(this).remove();
        });
        //Código para darle la habilidad al modal de cambiar la vista previa
        $("#imageUpload").change(function() {
            var reader = new FileReader();
            reader.onload = function(e) {
                $("#imagePreview").attr('src', e.target.result);
            };
            reader.readAsDataURL(this.files[0]);
        });
        $('#botonSubirProducto').on('click', function(e) {
            $('#modalCUD').modal('show');
            e.preventDefault();
            var form = $('#uploadForm')[0];
            var formData = new FormData(form);
            console.log(formData)
            $.ajax({
                url: BASE_URL + '/api/addProduct',  
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                    console.log(response)
                },
                error: function(xhr, status, error) {
                    console.log(xhr)
                    console.log(status)
                    console.log(error)
                }
            });
        });
    });
})



let currentYear = new Date().getFullYear();
document.getElementById("footer").innerHTML = `<div class="container text-center">
<span class="text-light">Copyright © ${currentYear} TiendaPET® Ltda.</span>
</div>`

if(window.location.pathname === '/contacto/') {
$('#formaContacto').validate({
    rules: {
        nombre: {
            required: true,
            minlength: 2
        },
        email: {
            required: true,
            email: true
        },
        razon: {
            required: true
        },
        comentario: {
            required: true,
            rangelength: [50, 700]
        },
        agree: {
            required: true
        }
    },
    messages: {
        nombre: "* El campo es obligatorio.",
        email: "* Debe escribir un correo electrónico válido.",
        razon: "* Debe seleccionar una opción de la lista.",
        comentario: "* Por favor, escriba al menos 50 carácteres y máximo 700.",
        agree: "* Debe aceptar nuestros términos y condiciones."
    },   
    submitHandler: function(form) {
        document.getElementById("formaContacto").reset();
      }
    
}
);
}

});


