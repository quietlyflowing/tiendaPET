$(document).ready(function () {
    console.log('App V2. Ready!')
    BASE_URL = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port;

    function login() {
        $.ajax({
            url: BASE_URL + "/ajax/login/",
            type: "POST",
            data: {
                email: $('#email').val(),
                password: $('#password').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (json) {
                $('#email').val('');
                $('#password').val('');
                console.log(json);
                $('#modalLogin').modal('hide');
                location.reload();
                console.log("success");

            },
            error: function (response) {
                if(response.status === 400){
                var content = 'Correo electrónico o contraseña inválidos';
                var elementoNuevo = $('<div>', {
                    'html': content,
                    'class': 'alert alert-warning',
                    'style': 'padding: .5rem;margin-top: .8rem; margin-bottom: -.1rem;',
                    'role': 'alert'
                }).hide();
                $('#modalContainer').append(elementoNuevo);
                elementoNuevo.fadeIn();
                $("input").on('keydown', function () {
                    elementoNuevo.fadeOut();
                });
            }
            if(response.status === 500){
                var content = 'Error interno del servidor. Intente más tarde.';
                var elementoNuevo = $('<div>', {
                    'html': content,
                    'class': 'alert alert-danger',
                    'style': 'padding: .5rem;margin-top: .8rem; margin-bottom: -.1rem;',
                    'role': 'alert'
                }).hide();
                $('#modalContainer').append(elementoNuevo);
                elementoNuevo.fadeIn();
                var timeOut = 3000
                setTimeout(function() {
                    $(elementoNuevo).fadeOut();
                  }, timeOut);
            }
            
        }
        });
    };

    //Procedimiento para añadir un listener que invoca el modal de inicio de sesión en la navbar
    $('#loginLink').on('click', function () {
        console.log('Abriendo modal de inicio de sesión.');
        $.get(BASE_URL + '/ajax/getModalLogin/', function (data) {
            $(data).appendTo('#tiendaNav');
            $('#modalLogin').modal('show');
            $('#anchorSignUp').on('click', function () {
                $('#modalLogin').modal('hide');
                window.location.href = '/signup/';
            });
            $('#iniciarSesion').click(function () {
                $('#loginForm').validate({
                    rules: {
                        email: {
                            required: true,
                            email: true,
                        },
                        password: {
                            required: true,
                            minlength: 8
                        }
                    }, messages: {
                        email: {
                            required: "* Debe escribir un correo electrónico válido.",
                            email: "* Debe introducir un correo electrónico válido."
                        },
                        password: {
                            required: "* Debe escribir su contraseña",
                            minlength: "* La contraseña debe tener mínimo 8 carácteres."
                        },
                    }
                });
                if ($('#loginForm').valid()) {
                    login();
                }
            });
            $('#modalLogin').on('hidden.bs.modal', function () {
                $(this).remove();
            })
        });
    });

    //Procedimiento para añadir un listener al botón de cerrar sesión
    $('#logoutLink').on('click', function () {
        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url: BASE_URL + '/ajax/logout/',
            headers: { 'X-CSRFToken': csrftoken },
            type: 'POST',
            success: function (response) {
                console.log(response);
                window.location.href = '/';
            }
        });
    });

    //Procedimiento para añadir un listener al botón con el nombre del usuario
    $('#userLink').on('click', function () {
        window.location.href = '/user/'
    });

    //Procedimiento que añade listeners al modal de carrito.
    $('.container').on('click', '#botonCarro', function () {
        console.log('Abriendo modal');
        $.get(BASE_URL + '/ajax/getModalCart/', function (data) {
            $(data).appendTo('#tiendaNav');
            $('#modalCarrito').modal('show');
            $('#modalCarrito').on('hidden.bs.modal', function (e) {
                $(this).remove();
                $.get(BASE_URL + '/ajax/cartButtonUpdate', function (data) {
                    console.log('Actualización del botón solicitada');
                    $('#indicadorCarrito').html(data);
                });
            });

            //Botón 3: Elimina la fila de la página de pago
            $("td > .btn.btn-danger").click(function () {
                // var carrito_id = 1 //hardcodeado por ahora
                var id_string = $(this).attr('id');
                var arrayString = id_string.split('_');
                var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
                $.ajax({
                    url: BASE_URL + '/ajax/removeAllTheSameItems/',
                    type: 'DELETE',
                    contentType: 'application/json',
                    headers: { 'X-CSRFToken': csrftoken },
                    data: JSON.stringify({ 'producto_id': arrayString[1] }),
                    success: function (response) {
                        $('#indicadorTotal').fadeToggle('fast', function () {
                            $(this).html('Total: $' + response.context.valor_total);
                        }).fadeToggle('fast');
                        $('#' + id_string).closest('tr').fadeOut('slow', function () {
                            $(this).remove();
                            if ($('#cuerpoTabla').children('tr').length == 0) {
                                $('.table').remove();
                                $('#indicadorTotal').remove();
                                $('.modal-footer').remove();
                                console.log('La tabla está vacía. Cerrando');
                                $('#modalCarrito').modal('hide');
                            }
                        });

                        $.get(BASE_URL + '/ajax/cartButtonUpdate', function (data) {
                            console.log('Actualización del botón solicitada');
                            $('#indicadorCarrito').html(data);
                        });
                    },
                    error: function (error) {
                        // Handle the error response
                        console.log('No se puede actualizar el carro.');
                    }
                });
            });
            //Fin listener botón 3
            //Botón 4: // Actualiza el carrito conforme se mueve las cantidades 
            $("td > .form-control").change(function () {
                var cantidad = $(this).val();
                var id_string = $(this).attr('id');
                var arrayString = id_string.split('_');
                var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
                var datos = {
                    producto_id: arrayString[1],
                    cantidad_producto: cantidad
                };
                $.ajax({
                    url: BASE_URL + '/ajax/updateItems',
                    type: 'PUT',
                    data: JSON.stringify(datos),
                    headers: { 'X-CSRFToken': csrftoken },
                    contentType: 'application/json',
                    success: function (response) {
                        $('#precioTotalID' + arrayString[1])
                            .fadeToggle('fast', function () {
                                $(this).html('$' + response.context.precio_total)
                            })
                            .fadeToggle('fast');
                        $('#indicadorTotal').fadeToggle('fast', function () {
                            $(this).html('Total: $' + response.context.valor_total);
                        }).fadeToggle('fast');


                        $.get(BASE_URL + '/ajax/cartButtonUpdate', function (data) {
                            console.log('Actualización del botón solicitada');
                            $('#indicadorCarrito').html(data);
                        });
                    }
                });
            });
            $('#killCarroStorage').on('click', function () {
                var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
                $.ajax({
                    url: BASE_URL + '/ajax/deleteEntireCart/',
                    headers: { 'X-CSRFToken': csrftoken },
                    type: 'DELETE',
                    success: function () {
                        $('.table').remove();
                        $('#modalCarrito').modal('hide');
                        $.get(BASE_URL + '/ajax/cartButtonUpdate', function (data) {
                            console.log('Actualización del botón solicitada');
                            $('#indicadorCarrito').html(data);
                        });
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            });


            $('#buttonCheckoOut').on('click', function () {
                console.log('Redirigiendo a checkout');
                window.location.href = '/checkout/'
            });
        });
    });
    //Fin del procedimiento que añade los listeners al modal

    //Procedimiento que añade listeners al botón Agregar al Carro de las cards.
    $("button").each(function () {
        if ($(this).parent().hasClass('card-body') && $(this).hasClass('btn-primary')) {
            $(this).click(function () {
                const grandParent = $(this).parent().parent().attr('id');
                var datos = { producto_id: grandParent, cantidad: 1 };
                var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
                //hardcodeado por ahora
                // $.post(BASE_URL + '/ajax/addItem', JSON.stringify(datos), function (response) {
                //     console.log(response);
                // }).done(function () {
                // $.get(BASE_URL + '/ajax/cartButtonUpdate', function (data) {
                //     console.log('Actualización del botón solicitada');
                //     $('#indicadorCarrito').html(data);
                // });
                // });
                $.ajax({
                    url: BASE_URL + '/ajax/addItem',
                    type: 'POST',
                    headers: { 'X-CSRFToken': csrftoken },
                    data: JSON.stringify({ producto_id: grandParent }),
                    contentType: 'application/json',
                    success: function (data) {
                        console.log(data);
                        $.get(BASE_URL + '/ajax/cartButtonUpdate', function (data) {
                            console.log('Actualización del botón solicitada');
                            $('#indicadorCarrito').html(data);
                        });
                    }
                });
            });
        }
    });
    //Fin del procedimiento que añade listeners a las cards.
    //Procedimiento que añade listeners al botón Eliminar de las cards
    $("button").each(function () {
        if ($(this).parent().hasClass('card-body') && $(this).text() === 'Eliminar') {
            $(this).click(function () {
                const grandParent = $(this).parent().parent().attr('id');
                $.get(BASE_URL + '/ajax/getModalConfirm', function (data) {
                    $(data).appendTo('#tiendaNav');
                    $('#modalConfirmacion').modal('show');
                    console.log("Modal de Confirmación solicitado")
                    $('#modalConfirmacion').on('hidden.bs.modal', function (e) {
                        $(this).remove();
                        $.get(BASE_URL + '/ajax/cartButtonUpdate', function (data) {
                            console.log('Actualización del botón solicitada');
                            $('#indicadorCarrito').html(data);
                        });
                    });
                    $('#confirmarEliminacion').on('click', function () {
                        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
                        $.ajax({
                            url: BASE_URL + '/ajax/removeProduct/',
                            type: 'DELETE',
                            headers: { 'X-CSRFToken': csrftoken },
                            data: JSON.stringify({ producto_id: grandParent }),
                            contentType: 'application/json',
                            success: function (data) {
                                console.log(data);
                                $('#cardGallery' + grandParent).fadeToggle('slow', function () {
                                    $(this).remove();
                                });
                                $('#modalConfirmacion').modal('hide');
                            }
                        });
                    });
                });
            });
        }
    });
    //fin procedimiento que añade listeners al botón Eliminar

    //Procedimiento que añade listeners al botón editar 

    $("button").each(function () {
        if ($(this).parent().hasClass('card-body') && $(this).text() === 'Editar') {
            $(this).on('click', function () {
                const grandParent = $(this).parent().parent().attr('id');
                console.log('Abriendo modal CUD');
                $.get(BASE_URL + '/ajax/getModalUpdate/' + grandParent, function (data) {
                    $(data).appendTo('#tiendaNav');
                    $('#modalCUD').modal('show');
                    $('#modalCUD').on('hidden.bs.modal', function (e) {
                        $(this).remove();
                    });
                    $("#imageUpload").change(function () {
                        var reader = new FileReader();
                        reader.onload = function (e) {
                            $("#imagePreview").attr('src', e.target.result);
                        };
                        reader.readAsDataURL(this.files[0]);
                    });
                    $('#botonSubirProducto').on('click', function (e) {

                        $('#modalCUD').modal('show');
                        e.preventDefault();
                        var form = $('#uploadForm')[0];
                        var formData = new FormData(form);
                        formData.append('producto_id', grandParent);
                        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
                        console.log(formData)
                        $.ajax({
                            url: BASE_URL + '/ajax/updateProduct/',
                            type: 'POST',
                            headers: { 'X-CSRFToken': csrftoken },
                            data: formData,
                            processData: false,
                            contentType: false,
                            success: function (response) {
                                console.log(response)
                            },
                            error: function (xhr, status, error) {
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
    $("button").each(function () {
        if ($(this).parent().hasClass('card-body') && $(this).text() === 'Ver') {
            $(this).click(function () {
                const grandParent = $(this).parent().parent().attr('id');
                $.get(BASE_URL + '/ajax/getModalProducto/' + grandParent, function (data) {
                    $(data).appendTo('#tiendaNav');
                    $('#modalProducto').modal('show');
                    $('#anadeProducto').click(function () {
                        var datos = { producto_id: grandParent, carrito_id: 1, cantidad: 1, cliente_id: 0 };
                        $.post(BASE_URL + '/ajax/addItem', JSON.stringify(datos), function (response) {
                            console.log(response);
                        }).done(function () {
                            $.get(BASE_URL + '/ajax/cartButtonUpdate', function (data) {
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
    $('#botonCrud').on('click', function () {
        console.log('Soy un botón para añadir productos');
        $.get(BASE_URL + '/ajax/getModalCUD', function (data) {
            console.log('Abriendo modal CUD');
            $(data).appendTo('#tiendaNav');
            $('#modalCUD').modal('show');
            $('#modalCUD').on('hidden.bs.modal', function (e) {
                $(this).remove();
            });
            //Código para darle la habilidad al modal de cambiar la vista previa
            $("#imageUpload").change(function () {
                var reader = new FileReader();
                reader.onload = function (e) {
                    $("#imagePreview").attr('src', e.target.result);
                };
                reader.readAsDataURL(this.files[0]);
            });
            $('#botonSubirProducto').on('click', function (e) {
                $('#modalCUD').modal('show');
                e.preventDefault();
                var form = $('#uploadForm')[0];
                var formData = new FormData(form);
                var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
                console.log(formData)

                $.ajax({
                    url: BASE_URL + '/ajax/addProduct',
                    type: 'POST',
                    headers: { 'X-CSRFToken': csrftoken },
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function (response) {
                        console.log(response)
                    },
                    error: function (xhr, status, error) {
                        console.log(xhr)
                        console.log(status)
                        console.log(error)
                    }
                });
            });
        });
    })


    if (window.location.pathname !== '/donar/') {
        let currentYear = new Date().getFullYear();
        document.getElementById("footer").innerHTML = `<div class="container text-center">
<span class="text-light">Copyright © ${currentYear} TiendaPET® Ltda.</span>
</div>`
    }





    if (window.location.pathname === '/contacto/') {
        function ajaxFormContact() {
            var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
            $.ajax({
                url: $('#formaContacto').attr('action'),
                type: $('#formaContacto').attr('method'),
                data: $('#formaContacto').serialize(),
                headers: { 'X-CSRFToken': csrftoken },
                success: function (response) {
                    console.log(response);
                    var datos = { titulo_modal: 'Mensaje enviado', mensaje_modal: 'Su mensaje ha sido enviado correctamente. Pronto tendrá noticias de nosotros.' };
                    $.ajax({
                        url: BASE_URL + '/ajax/getModalErrores/',
                        type: 'POST',
                        contentType: 'application/json',
                        headers: { 'X-CSRFToken': csrftoken },
                        data: JSON.stringify(datos),
                        success: function (response) {
                            $(response).appendTo('#tiendaNav');
                            $('#modalErrores').modal('show');
                            $('#modalErrores').on('hidden.bs.modal', function (e) {
                                $(this).remove();
                            });
                        },
                        error: function (error) {
                            console.log(error);
                        }
                    });
                },

                error: function (xhr, errmsg, err) {
                    console.log(xhr)
                    var datos = { titulo_modal: 'Error', mensaje_modal: 'Ocurrió un error. Por favor, intente enviar su mensaje más tarde' };
                    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
                    $.ajax({
                        url: BASE_URL + '/ajax/getModalErrores/',
                        type: 'POST',
                        contentType: 'application/json',
                        headers: { 'X-CSRFToken': csrftoken },
                        data: JSON.stringify(datos),
                        success: function (response) {
                            $(response).appendTo('#tiendaNav');
                            $('#modalErrores').modal('show');
                            $('#modalErrores').on('hidden.bs.modal', function (e) {
                                $(this).remove();
                            });
                        },
                        error: function (error) {
                            // Handle the error response
                            console.log(error);
                        }
                    });

                }
            });
        }
        $('#botonEnviar').on('click', function () {
            $('#formaContacto').validate({
                rules: {
                    nombre: {
                        required: true,
                        minlength: 2,
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
                }
            });
            if ($('#formaContacto').valid()) {
                ajaxFormContact();
            }

        });




    }
    if (window.location.pathname === '/donar/') {

        function ajaxFormDonar() {
            var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
            $.ajax({
                url: $('#formaDonacion').attr('action'),
                type: $('#formaDonacion').attr('method'),
                data: $('#formaDonacion').serialize(),
                headers: { 'X-CSRFToken': csrftoken },
                success: function (response) {
                    console.log(response);
                    $.get(BASE_URL + '/ajax/getModalDonacion/', function (data) {
                        $(data).appendTo('#tiendaNav');
                        $('#modalDonacion').modal('show');
                        $('#modalDonacion').on('hidden.bs.modal', function (e) {
                            $(this).remove();
                            window.location.href = '/';
                        });
                    });
                },

                error: function (xhr, errmsg, err) {
                    console.log(xhr)
                    var datos = { titulo_modal: 'Error', mensaje_modal: 'Ocurrió un error. Por favor, intente realizar su donación más tarde' };
                    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
                    $.ajax({
                        url: BASE_URL + '/ajax/getModalErrores/',
                        type: 'POST',
                        contentType: 'application/json',
                        headers: { 'X-CSRFToken': csrftoken },
                        data: JSON.stringify(datos),
                        success: function (response) {
                            $(response).appendTo('#tiendaNav');
                            $('#modalErrores').modal('show');
                            $('#modalErrores').on('hidden.bs.modal', function (e) {
                                $(this).remove();
                            });
                        },
                        error: function (error) {
                            // Handle the error response
                            console.log(error);
                        }
                    });

                }
            });
        }
        $.validator.addMethod('pattern', function (value, element, param) {
            return this.optional(element) || param.test(value);
        }, 'Invalid format.');
        $('#botonDonar').on('click', function () {
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
                        maxlength: 40,
                        pattern: new RegExp("^(?=.{1,40}$)[a-zA-ZáéíóúüñÁÉÍÓÚÑ]+(?:[\\s][a-zA-ZáéíóúüñÁÉÍÓÚÑ]+)*$")
                    },
                    apellido: {
                        required: true,
                        minlength: 3,
                        maxlength: 40,
                        pattern: new RegExp("^(?=.{1,40}$)[a-zA-ZáéíóúüñÁÉÍÓÚÑ]+(?:[\\s][a-zA-ZáéíóúüñÁÉÍÓÚÑ]+)*$")
                    },
                    rut: {
                        required: true,
                        pattern: new RegExp("^\\d\\d?\\.?\\d{3}\\.?\\d{3}\\-[kK\\d]$")
                    },
                    correo: {
                        required: true,
                        email: true,
                        maxlength: 35
                    },
                    celular: {
                        required: true,
                        minlength: 9,
                        maxlength: 12
                    },
                    optradio: {
                        required: true
                    },
                    titular: {
                        required: true,
                        pattern: new RegExp("^(?=.{1,40}$)[a-zA-ZáéíóúüñÁÉÍÓÚÑ]+(?:[\\s][a-zA-ZáéíóúüñÁÉÍÓÚÑ]+)*$")
                    },
                    numero: {
                        required: true,
                        minlength: 16,
                        maxlength: 19
                    },
                    codigo: {
                        required: true,
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
                    correo: "* Debe introducir su correo electrónico",
                    celular: "* El celular debe tener de 9 a 12 caracteres",
                    optradio: "* Debe seleccionar un método de pago",
                    titular: "* Debe ingresar un nombre válido",
                    numero: "* El número de tarjeta no es válido",
                    codigo: "* Debe ingresar un código válido de 3 dígitos",
                    fecha: "* Debe ingresar una fecha válida entre 2024 y 2045"
                }
            });
            if ($('#formaDonacion').valid()) {
                ajaxFormDonar();
            }
        });

        console.log('Listo para actuar en donar/')
    }

    if (window.location.pathname === '/checkout/') {

        function ajaxFormCheckout() {
            var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
            $.ajax({
                url: $('#formaCheckout').attr('action'),
                type: $('#formaCheckout').attr('method'),
                data: $('#formaCheckout').serialize(),
                headers: { 'X-CSRFToken': csrftoken },
                success: function (response) {
                    var datos = { titulo_modal: '¡Compra realizada!', mensaje_modal: 'Su compra ha sido realizada correctamente. Pronto recibirá un correo electrónico con los detalles de su compra.' };
                    console.log(response);
                    $.ajax({
                        url: BASE_URL + '/ajax/getModalErrores/',
                        type: 'POST',
                        contentType: 'application/json',
                        headers: { 'X-CSRFToken': csrftoken },
                        data: JSON.stringify(datos),
                        success: function (response) {
                            $(response).appendTo('#tiendaNav');
                            $('#modalErrores').modal('show');
                            $('#modalErrores').on('hidden.bs.modal', function () {
                                $(this).remove();
                                window.location.href = '/';
                            });
                        },
                        error: function (error) {
                            // Handle the error response
                            console.log(error);
                        }
                    });
                },

                error: function (xhr, errmsg, err) {
                    console.log(xhr)
                    var datos = { titulo_modal: 'Error', mensaje_modal: 'Ocurrió un error. Por favor, intente realizar su donación más tarde' };
                    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
                    $.ajax({
                        url: BASE_URL + '/ajax/getModalErrores/',
                        type: 'POST',
                        contentType: 'application/json',
                        headers: { 'X-CSRFToken': csrftoken },
                        data: JSON.stringify(datos),
                        success: function (response) {
                            $(response).appendTo('#tiendaNav');
                            $('#modalErrores').modal('show');
                            $('#modalErrores').on('hidden.bs.modal', function () {
                                $(this).remove();
                            });
                        },
                        error: function (error) {
                            // Handle the error response
                            console.log(error);
                        }
                    });

                }
            });
        }

        $('#botonPagar').on('click', function () {
            $('#formaCheckout').validate({
                rules: {
                    nombre: {
                        required: true,
                        minlength: 2
                    },
                    email: {
                        required: true,
                        email: true
                    },
                    direccion: {
                        required: true
                    },
                    ciudad: {
                        required: true
                    },
                    region: {
                        required: true
                    },
                    optradio: {
                        required: true
                    },
                    titular: {
                        required: true,
                        minlength: 2
                    },
                    numero: {
                        rangelength: [16, 19]
                    }

                },
                messages: {
                    nombre: "* El campo es obligatorio.",
                    email: "* Debe escribir un correo electrónico válido.",
                    direccion: "* Debe proporcionar su dirección.",
                    ciudad: "* Debe proporcionar su ciudad.",
                    region: "* Debe seleccionar su región.",
                    optradio: "* Debe seleccionar un método de pago.",
                    titular: "* El campo es obligatorio.",
                    numero: "* El número de su tarjeta debe contener de 16 a 19 números.",
                    codigo: "* El código de seguridad de su tarjeta debe ser de 3 números.",
                    fecha: "* Debe introducir la fecha de vencimiento de su tarjeta."

                }
            });
            if ($('#formaCheckout').valid()) {
                ajaxFormCheckout();
            }
        });



    }

    if (window.location.pathname === '/signup/') {
        //Producedimiento para crear el listener para la región
        // $('#selectorRegion').on('change', function() {
        //     regionId = $(this).val();
        //     alert(regionId);
        //     $.getJSON(BASE_URL+'/ajax/getComunas/'+regionId, function(data) {
        //         $.each(data, function(index) {
        //             console.log(data[index].nombre);
        //         });
        //     });
        // })


        function ajaxFormSignup() {
            var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
            $.ajax({
                url: $('#formaRegistro').attr('action'),
                type: $('#formaRegistro').attr('method'),
                data: $('#formaRegistro').serialize(),
                headers: { 'X-CSRFToken': csrftoken },
                success: function (response) {
                    var datos = { titulo_modal: '¡Registro completo!', mensaje_modal: 'Usted se ha registrado correctamente. Ahora puede iniciar sesión.' };
                    console.log(response);
                    $.ajax({
                        url: BASE_URL + '/ajax/getModalErrores/',
                        type: 'POST',
                        contentType: 'application/json',
                        headers: { 'X-CSRFToken': csrftoken },
                        data: JSON.stringify(datos),
                        success: function (response) {
                            $(response).appendTo('#tiendaNav');
                            $('#modalErrores').modal('show');
                            $('#modalErrores').on('hidden.bs.modal', function () {
                                $(this).remove();
                                window.location.href = '/';
                            });
                        },
                        error: function (error) {
                            // Handle the error response
                            console.log(error);
                        }
                    });
                },

                error: function (xhr, errmsg, err) {
                    console.log(xhr)
                    var datos = { titulo_modal: 'Error', mensaje_modal: 'Ocurrió un error. Por favor, intente registrarse más tarde.' };
                    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
                    $.ajax({
                        url: BASE_URL + '/ajax/getModalErrores/',
                        type: 'POST',
                        contentType: 'application/json',
                        headers: { 'X-CSRFToken': csrftoken },
                        data: JSON.stringify(datos),
                        success: function (response) {
                            $(response).appendTo('#tiendaNav');
                            $('#modalErrores').modal('show');
                            $('#modalErrores').on('hidden.bs.modal', function () {
                                $(this).remove();
                            });
                        },
                        error: function (error) {
                            // Handle the error response
                            console.log(error);
                        }
                    });

                }
            });
        }

        $('#botonRegistro').on('click', function () {
            $('#formaRegistro').validate(
                {
                    rules: {
                        primer_nombre: {
                            required: true,
                            minlength: 3
                        },
                        segundo_nombre: {
                            required: false,
                            minlength: 3
                        },
                        primer_apellido: {
                            required: true,
                        },
                        segundo_apellido: {
                            required: false,
                        },
                        rut: {
                            required: true,
                            minlength: 9,
                            maxlength: 10
                        },
                        correo: {
                            required: true,
                            email: true
                        },
                        direccion: {
                            required: true,
                            minlength: 10,
                        },
                        password: {
                            required: true,
                            minlength: 8,
                            maxlength: 15
                        },
                        confirm_password: {
                            required: true,
                            equalTo: "#password",
                            minlength: 8,
                            maxlength: 15
                        },
                        comuna: {
                            required: true
                        }

                    },
                    messages: {
                        primer_nombre: {
                            required: "* El campo es obligatorio.",
                            minlength: "* El nombre debe tener al menos 3 carácteres."
                        },
                        primer_apellido: {
                            required: "* El campo es obligatorio.",
                            minlength: "* El primer apellido debe tener al menos 3 carácteres."
                        },
                        correo: {
                            required: "* Debe escribir un correo electrónico válido.",
                            email: "* Debe introducir un correo electrónico válido."
                        },
                        direccion: {
                            required: "* Debe proporcionar su dirección.",
                            minlength: "* La dirección debe tener al menos 10 carácteres."
                        },
                        region: {
                            required: "* Debe seleccionar su región."
                        },
                        password: {
                            required: "* Debe ingresar una contraseña.",
                            minlength: "* La contraseña debe tener mínimo 8 carácteres.",
                            maxlength: "* La contraseña debe no debe tener más de 15 carácteres."
                        },
                        confirm_password: {
                            required: "* Debe volver a escribir su contraseña.",
                            minlength: "* La contraseña debe tener mínimo 8 carácteres.",
                            maxlength: "* La contraseña debe no debe tener más de 15 carácteres.",
                            equalTo: "* Las contraseñas no coinciden."
                        },
                        rut: {
                            required: "* El RUT es obligatorio.",
                            minlength: "* El RUT debe tener al menos ocho carácteres."
                        },
                        comuna: {
                            required: "* Debe seleccionar su comuna",
                            notEqual: "* Debe seleccionar su comuna"
                        }
                    }
                });
            if ($('#formaRegistro').valid()) {
                ajaxFormSignup();
            }
        });
        jQuery.validator.addMethod("notEqualTo", function(v, e, p) {  
            return this.optional(e) || v != p;
          }, "* Debe escojer su comuna");
    }

    if(window.location.pathname === '/user/'){

        function ajaxUpdateDatos() {
            var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
            $.ajax({
                url: $('#formaUpdate').attr('action'),
                type: 'POST',
                data: $('#formaUpdate').serialize(),
                headers: { 'X-CSRFToken': csrftoken },
                success: function (response) {
                    
                    var datos = { titulo_modal: 'Actualización realizada', mensaje_modal: '¡Datos actualizados correctamente!' };
                    console.log(response);
                    $.ajax({
                        url: BASE_URL + '/ajax/getModalErrores/',
                        type: 'POST',
                        contentType: 'application/json',
                        headers: { 'X-CSRFToken': csrftoken },
                        data: JSON.stringify(datos),
                        success: function (response) {
                            $(response).appendTo('#tiendaNav');
                            $('#modalErrores').modal('show');
                            $('#modalErrores').on('hidden.bs.modal', function () {
                                $(this).remove();
                                location.reload();
                            });
                        },
                        error: function (error) {
                            console.log(error);
                        }
                    });
                },

                error: function (xhr, errmsg, err) {
                    console.log(xhr)
                    var datos = { titulo_modal: 'Error', mensaje_modal: 'Ocurrió un error. Por favor, intente actualizar sus datos más tarde.' };
                    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
                    $.ajax({
                        url: BASE_URL + '/ajax/getModalErrores/',
                        type: 'POST',
                        contentType: 'application/json',
                        headers: { 'X-CSRFToken': csrftoken },
                        data: JSON.stringify(datos),
                        success: function (response) {
    
                            $(response).appendTo('#tiendaNav');
                            $('#modalErrores').modal('show');
                            $('#modalErrores').on('hidden.bs.modal', function () {
                                $(this).remove();
                            });
                        },
                        error: function (error) {
                            console.log(error);
                        }
                    });

                }
            });
        }

        function ajaxUpdatePassword() {
            var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
            $.ajax({
                url: BASE_URL+'/ajax/changePass/',
                type: 'POST',
                data: $('#changePassForm').serialize(),
                headers: { 'X-CSRFToken': csrftoken },
                success: function (response) {
                    if(response.message === 'ok'){
                    $('#modalChangePass').modal('hide');
                    var datos = { titulo_modal: 'Actualización realizada', mensaje_modal: '¡Su contraseña ha sido actualizada exitosamente!' };
                    console.log(response);
                    $.ajax({
                        url: BASE_URL + '/ajax/getModalErrores/',
                        type: 'POST',
                        contentType: 'application/json',
                        headers: { 'X-CSRFToken': csrftoken },
                        data: JSON.stringify(datos),
                        success: function (response) {
                            $(response).appendTo('#tiendaNav');
                            $('#modalErrores').modal('show');
                            $('#modalErrores').on('hidden.bs.modal', function () {
                                $(this).remove();
                            });
                        },
                        error: function (error) {
                            console.log(error);
                        }
                    });
                }
                    if(response.message === 'same_pass'){
                        var content = 'La contraseña nueva es la misma que la anterior.';
                        var elementoNuevo = $('<div>', {
                            'html': content,
                            'class': 'alert alert-warning',
                            'style': 'padding: .5rem;margin-top: .8rem; margin-bottom: -.1rem;',
                            'role': 'alert'
                        }).hide();
                        $('#modalContainer').append(elementoNuevo);
                        elementoNuevo.fadeIn();
                        var timeOut = 3000
                        setTimeout(function() {
                            $(elementoNuevo).fadeOut();
                          }, timeOut);
                    }
                    if(response.message === 'invalid_pass'){
                        var content = 'La antigua contraseña no es válida.';
                        var elementoNuevo = $('<div>', {
                            'html': content,
                            'class': 'alert alert-warning',
                            'style': 'padding: .5rem;margin-top: .8rem; margin-bottom: -.1rem;',
                            'role': 'alert'
                        }).hide();
                        $('#modalContainer').append(elementoNuevo);
                        elementoNuevo.fadeIn();
                        var timeOut = 3000
                        setTimeout(function() {
                            $(elementoNuevo).fadeOut();
                          }, timeOut);
                    }
                },

                error: function (response) {
                    console.log(response)
                    // var datos = { titulo_modal: 'Error', mensaje_modal: 'Ocurrió un error. Por favor, intente actualizar sus datos más tarde.' };
                    // var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
                    // $.ajax({
                    //     url: BASE_URL + '/ajax/getModalErrores/',
                    //     type: 'POST',
                    //     contentType: 'application/json',
                    //     headers: { 'X-CSRFToken': csrftoken },
                    //     data: JSON.stringify(datos),
                    //     success: function (response) {
                    //         $(response).appendTo('#tiendaNav');
                    //         $('#modalErrores').modal('show');
                    //         $('#modalErrores').on('hidden.bs.modal', function () {
                    //             $(this).remove();
                    //         });
                    //     },
                    //     error: function (error) {
                    //         console.log(error);
                    //     }
                    // });
                    if(response.status === 500){
                        var content = 'Error interno del servidor. Intente más tarde.';
                        var elementoNuevo = $('<div>', {
                            'html': content,
                            'class': 'alert alert-danger',
                            'style': 'padding: .5rem;margin-top: .8rem; margin-bottom: -.1rem;',
                            'role': 'alert'
                        }).hide();
                        $('#modalContainer').append(elementoNuevo);
                        elementoNuevo.fadeIn();
                        var timeOut = 3000
                        setTimeout(function() {
                            $(elementoNuevo).fadeOut();
                          }, timeOut);
                    }
                }
            });
        }

        $('#botonGuardado').on('click', function () {
            $('#formaUpdate').validate(
                {
                    rules: {
                        primer_nombre: {
                            required: true,
                            minlength: 3
                        },
                        segundo_nombre: {
                            required: false,
                            minlength: 3
                        },
                        primer_apellido: {
                            required: true,
                        },
                        segundo_apellido: {
                            required: false,
                        },
                        correo: {
                            required: true,
                            email: true
                        },
                        direccion: {
                            required: true,
                            minlength: 10,
                        },
                        comuna: {
                            required: true
                        }

                    },
                    messages: {
                        primer_nombre: {
                            required: "* El campo es obligatorio.",
                            minlength: "* El nombre debe tener al menos 3 carácteres."
                        },
                        primer_apellido: {
                            required: "* El campo es obligatorio.",
                            minlength: "* El primer apellido debe tener al menos 3 carácteres."
                        },
                        correo: {
                            required: "* Debe escribir un correo electrónico válido.",
                            email: "* Debe introducir un correo electrónico válido."
                        },
                        direccion: {
                            required: "* Debe proporcionar su dirección.",
                            minlength: "* La dirección debe tener al menos 10 carácteres."
                        },
                        region: {
                            required: "* Debe seleccionar su región."
                        },
                        password: {
                            required: "* Debe ingresar una contraseña.",
                            minlength: "* La contraseña debe tener mínimo 8 carácteres.",
                            maxlength: "* La contraseña debe no debe tener más de 15 carácteres."
                        },
                        confirm_password: {
                            required: "* Debe volver a escribir su contraseña.",
                            minlength: "* La contraseña debe tener mínimo 8 carácteres.",
                            maxlength: "* La contraseña debe no debe tener más de 15 carácteres.",
                            equalTo: "* Las contraseñas no coinciden."
                        },
                        rut: {
                            required: "* El RUT es obligatorio.",
                            minlength: "* El RUT debe tener al menos ocho carácteres."
                        },
                        comuna: {
                            required: "* Debe seleccionar su comuna",
                            notEqual: "* Debe seleccionar su comuna"
                        }
                    }
                });
            if ($('#formaUpdate').valid()) {
                ajaxUpdateDatos();
            }
        });

        $('#botonContrasena').on('click', function(){
            $.get(BASE_URL+'/ajax/getModalPass/', function(data){
                $(data).appendTo('#tiendaNav');
                $('#modalChangePass').modal('show');
                $('#modalChangePass').on('hidden.bs.modal', function (e) {
                    $(this).remove();});
                $('#closeModal').on('click', function(){
                    $('#modalChangePass').modal('hide');
                });
                $('#confirmChange').on('click', function(){
                    $('#changePassForm').validate({
                        rules:{
                            oldpassword: {
                                required: true,
                                minlength: 8,
                                maxlength: 15
                            },
                            newpassword: {
                                required: true,
                                minlength: 8,
                                maxlength: 15
                            },
                            checkpassword: {
                                required: true,
                                minlength: 8,
                                maxlength: 15, 
                                equalTo: "#newpassword"
                            }
                        }, messages: {
                            oldpassword: {
                                required: "* Debe ingresar una contraseña.",
                                minlength: "* La contraseña debe tener mínimo 8 carácteres.",
                                maxlength: "* La contraseña debe no debe tener más de 15 carácteres."
                            },
                            newpassword: {
                                required: "* Debe ingresar una contraseña.",
                                minlength: "* La contraseña debe tener mínimo 8 carácteres.",
                                maxlength: "* La contraseña debe no debe tener más de 15 carácteres."
                            },
                            checkpassword: {
                                required: "* Debe ingresar una contraseña.",
                                minlength: "* La contraseña debe tener mínimo 8 carácteres.",
                                maxlength: "* La contraseña debe no debe tener más de 15 carácteres.",
                                equalTo: "* Las contraseñas no coinciden."
                            },
                        }

                    });
                    if ($('#changePassForm').valid()) {
                    $(this).text('¿Está seguro?');
                    $(this).off('click');
                    $(this).attr('id', 'sendChange');
                    $('#sendChange').on('click', function() {
                        
                        ajaxUpdatePassword();
                        
                    });
                }
                });


            });
        });


    }

});


