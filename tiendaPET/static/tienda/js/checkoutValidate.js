const modalEnviado = new bootstrap.Modal(document.getElementById('modalCheckout'));
const modalEnviadoEl = document.getElementById('modalCheckout');
modalEnviadoEl.addEventListener('hidden.bs.modal', event => {
    window.location.replace("index.html");
  });
  
function modalDisplay() {
    console.log('Su dinero ha sido enviado a /dev/null');
    modalEnviado.show();
    document.getElementById("formaCheckout").reset(); //Por algún motivo, seleccionar esto por jQuery genera un error.
}



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
            rangelength: [16,19]
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

    },   
    submitHandler: function(form) {
       modalDisplay();
      }
    
}
);
