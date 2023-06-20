const modalEnviado = new bootstrap.Modal(document.getElementById('modalEnviado'));
const modalEnviadoEl = document.getElementById('modalEnviado');
modalEnviadoEl.addEventListener('hidden.bs.modal', event => {
    window.location.replace("index.html");
  });
  
function modalDisplay() {
    console.log('Su mensaje ha sido enviado con cariño a /dev/null');
    modalEnviado.show();
    document.getElementById("formaContacto").reset(); //Por algún motivo, seleccionar esto por jQuery genera un error.
}


var validator = $('#formaContacto').validate({
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
       modalDisplay();
      }
    
}
);