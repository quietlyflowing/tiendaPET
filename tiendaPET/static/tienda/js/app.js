$(document).ready(function() {
BASE_URL = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port;

function login() {
    $.ajax({
        url : BASE_URL + "/ajax/login/",
        type : "POST", 
        data : { 
            email : $('#email').val(), 
            password : $('#password').val(), 
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val() 
        }, 

       
        success : function(json) {
            $('#email').val(''); 
            $('#password').val(''); 
            console.log(json); 
            $('#modalLogin').modal('hide');
            console.log("success");

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

//Procedimiento para añadir un listener que invoca el modal de inicio de sesión en la navbar
$('#loginLink').on('click', function() {
    console.log('Abriendo modal de inicio de sesión.');
    $.get(BASE_URL+'/ajax/getModalLogin/', function(data){
        $(data).appendTo('#tiendaNav');
        $('#modalLogin').modal('show');
        $('#iniciarSesion').click( function() {
            login();
            console.log('Forma enviada!');
            
        });
        $('#modalLogin').on('hidden.bs.modal', function(e){
            $(this).remove();
            console.log('Acá invocamos el código para actualizar la Navbar para que nos muestre el log');
        })
    });
});



//Procedimiento que añade listeners al modal de carrito.
$('.container').on('click', '#botonCarro', function() {
    console.log('Abriendo modal');
    $.get(BASE_URL+'/ajax/getModalCart/', function(data) {
        $(data).appendTo('#tiendaNav');
        $('#modalCarrito').modal('show');
        $('#modalCarrito').on('hidden.bs.modal', function(e) {
            $(this).remove();
            $.get(BASE_URL + '/ajax/cartButtonUpdate', function(data) {
                console.log('Actualización del botón solicitada');
                $('#indicadorCarrito').html(data);});});

              //Botón 3: Elimina la fila de la página de pago
              $("td > .btn.btn-danger").click(function() {
                var carrito_id = 1 //hardcodeado por ahora
                var id_string = $(this).attr('id');
                var arrayString = id_string.split('_');
                 $.get(BASE_URL+'/ajax/removeAllTheSameItems/'+carrito_id + '/' +arrayString[1]+ '/', function(data){
                     console.log(data)
                     $('#'+id_string).closest('tr').remove();
                     if ($('#cuerpoTabla').children('tr').length === 0) {
                        $('.table').remove();
                        console.log('La tabla está vacía. Cerrando');
                        $('#modalCarrito').modal('hide');
                    }
                     $.get(BASE_URL + '/ajax/cartButtonUpdate', function(data) {
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
                $.post(BASE_URL + '/ajax/updateItems', JSON.stringify(datos), function() {
                    $.get(BASE_URL + '/ajax/getCartStats', function(data) {
                        console.log(data);
                    });
                    $.get(BASE_URL + '/ajax/cartButtonUpdate', function(data) {
                        console.log('Actualización del botón solicitada');
                        $('#indicadorCarrito').html(data);
                    });
                });
            });
            //Fin Botón 4:
            //Botón 5: Elimina el carrito y cierra el modal.
            $('#killCarroStorage').on('click', function() {
                $.get(BASE_URL+'/ajax/deleteEntireCart/1', function() {
                    $('.table').remove();
                    $('#modalCarrito').modal('hide');
                    $.get(BASE_URL + '/ajax/cartButtonUpdate', function(data) {
                        console.log('Actualización del botón solicitada');
                        $('#indicadorCarrito').html(data);
                    });
                });
            });
            $('#buttonCheckoOut').on('click', function() {
                console.log('Redirigiendo a checkout');
                window.location.href='/checkout/'
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
            $.post(BASE_URL+'/ajax/addItem', JSON.stringify(datos), function(response) {
                console.log(response);
            }).done(function(){  $.get(BASE_URL+'/ajax/cartButtonUpdate', function(data){ 
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
            const grandParent = $(this).parent().parent().attr('id');
            $.get(BASE_URL+'/ajax/getModalConfirm', function(data) {
                $(data).appendTo('#tiendaNav');
                $('#modalConfirmacion').modal('show');
                console.log("Modal de Confirmación solicitado")
                $('#modalConfirmacion').on('hidden.bs.modal', function(e) {
                    $(this).remove();
                    $.get(BASE_URL + '/ajax/cartButtonUpdate', function(data) {
                        console.log('Actualización del botón solicitada');
                        $('#indicadorCarrito').html(data);});});
                $('#confirmarEliminacion').on('click', function() {
                   $('#cardGallery'+grandParent).remove();
                   $('#modalConfirmacion').modal('hide');
                   $.get(BASE_URL + '/ajax/removeProduct/'+grandParent, function(data){
                        console.log(data);
                   });
                });
            });
        });
    }});
//fin procedimiento que añade listeners al botón Eliminar

//Procedimiento que añade listeners al botón editar 

$("button").each(function(){
    if($(this).parent().hasClass('card-body') && $(this).text() === 'Editar') {
         $(this).on('click', function() {
            const grandParent = $(this).parent().parent().attr('id');
            console.log('Abriendo modal CUD');
            $.get(BASE_URL + '/ajax/getModalUpdate/'+grandParent, function(data){
                $(data).appendTo('#tiendaNav');
                $('#modalCUD').modal('show');
                $('#modalCUD').on('hidden.bs.modal', function(e) {
                    $(this).remove();
                });
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
                            url: BASE_URL + '/ajax/updateProduct/' + grandParent,  
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
     });
 }
 }
 );

//Procedimiento que crea listeners en los botones ver
$("button").each(function(){
    if($(this).parent().hasClass('card-body') && $(this).text() === 'Ver') {
        $(this).click(function() {
            const grandParent = $(this).parent().parent().attr('id');
            $.get(BASE_URL+'/ajax/getModalProducto/'+grandParent, function(data){
                $(data).appendTo('#tiendaNav');
                $('#modalProducto').modal('show');
                $('#anadeProducto').click(function() {
                    var datos = {producto_id: grandParent, carrito_id: 1, cantidad:1, cliente_id: 0};
                    $.post(BASE_URL+'/ajax/addItem', JSON.stringify(datos), function(response) {
                        console.log(response);
                    }).done(function(){  $.get(BASE_URL+'/ajax/cartButtonUpdate', function(data){ 
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
    $.get(BASE_URL + '/ajax/getModalCUD', function(data) {
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
                url: BASE_URL + '/ajax/addProduct',  
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
if(window.location.pathname === '/donar/') {
    $.validator.addMethod('pattern', function(value, element, param) {
        return this.optional(element) || param.test(value);
    }, 'Invalid format.');
    $('#formaDonacion').validate({
        rules: {
            cantidad: {
                required: true,
                min: 1000,
                max: 1000000
            },
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 15
            },
            apellido: {
                required: true,
                minlength: 3,
                maxlength: 15
            },
            rut: {
                required: true,
                pattern: "\\d{7,8}-[0-9kK]{1}"
            },
            email: {
                required: true,
                email: true,
                maxlength: 35
            },
            celular: {
                required: true,
                pattern: "(56|9)(\d{8}|\d{9})"
            },
            optradio: {
                required: true
            },
            titular: {
                required: true,
                pattern: "^[a-zA-ZÀ-ÖØ-öø-ÿ\s.'-]{1,40}$"
            },
            numero: {
                required: true,
                pattern: "[0-9]{4}?[0-9]{4}?[0-9]{4}?[0-9]{4}",
                minlength: 16,
                maxlength: 19
            },
            codigo: {
                required: true,
                pattern: "^[0-9]{3}",
                minlength: 3,
                maxlength: 3
            },
            fecha: {
                required: true,
                date: true,
                min: "2024-01",
                max: "2045-12"
            }
        },
        messages: {
            cantidad: "* La donación debe ser de entre $1.000 a $1.000.000",
            nombre: "* El Nombre debe tener entre 3 a 15 caracteres",
            apellido: "* El apellido debe tener entre 3 y 15 caracteres",
            rut: "* El RUT debe tener de 9 a 10 caracteres",
            email: "* Debe introducir su correo electrónico",
            celular: "* El celular debe tener de 9 a 12 caracteres",
            optradio: "* Debe seleccionar un método de pago",
            titular: "* Debe ingresar un nombre válido",
            numero: "* El número de tarjeta no es válido",
            codigo: "* Debe ingresar un código válido de 3 dígitos",
            fecha: "* Debe ingresar una fecha válida entre 2024 y 2045"
        },
        submitHandler: function(form) {
            document.getElementById("formaDonacion").reset();
        }
    });
    
}
console.log('App V2. Ready!')

});


