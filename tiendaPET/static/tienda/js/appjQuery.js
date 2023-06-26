$(document).ready(function(){
const cart = JSON.parse(localStorage.getItem('cart')) || [];
const windowTitle = $(document).attr('title');

//Crea el indicador del carrito
function indicadorCarro() {
$('#indicadorCarrito').empty();
const totalQuantity = cart.reduce((accumulator, item) => accumulator + item.cantidad, 0);
$('#indicadorCarrito').append(`<button class="btn btn-primary d-flex align-items-center" id="botonCarro" style="padding: .75rem;">
<i class="fas fa-shopping-cart ms-2 mb-0"></i> <p class="m-0 me-2"><strong style="margin-left: .75rem;">Carrito: ${totalQuantity}</strong></p> </button>`);
$('#botonCarro').on("click", function() {
    viewCart();
  });

}
indicadorCarro();
console.log("ready!");

function showCurrentYearFooter() {
//Muestra la fecha actual en el documento HTML
//Esto perfectamente podría estar suelto, pero meh.
let currentYear = new Date().getFullYear();
document.getElementById("footer").innerHTML = `<div class="container text-center">
<span class="text-light">Copyright © ${currentYear} TiendaPET® Ltda.</span>
</div>`}

showCurrentYearFooter();


const aviso = (message, type) => {
    alertPlaceholder = $('#liveAlertPlaceholder');
    const wrapper = document.createElement('div');
    wrapper.innerHTML = [
      `<div class="alert alert-${type} alert-dismissible" role="alert">`,
      `   <div>${message}</div>`,
      '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
      '</div>'
    ].join('');
  
    alertPlaceholder.append(wrapper);
  }


function itemExiste(id) {
    return cart.findIndex(item => item.id === id) !== -1;
}

function actualizaCarro(item) {
    const existingItemIndex = cart.findIndex(existingItem => existingItem.id === item.id);
    if (existingItemIndex !== -1) {
        // Item already exists in the cart, update the quantity and total_price
        cart[existingItemIndex].cantidad += 1;
        cart[existingItemIndex].precio_total = cart[existingItemIndex].cantidad * item.precio;
      } else {
        // Item doesn't exist in the cart, add it with the additional fields
        const newItem = {
          ...item,
          cantidad: 1,
          precio_total: item.precio
        };
        cart.push(newItem);
      }
      localStorage.setItem('cart', JSON.stringify(cart));
      indicadorCarro();
}


function viewElement(id){ 
   const producto = productosTienda.find(obj => obj.id == id);
    $('#modalProducto').append(`<div class="modal-dialog modal-dialog-centered modal-dialog-scrollable"" data-bs-backdrop="static" data-bs-keyboard="false" id="tempModal">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5">${producto.nombre}</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <img src="${producto.imagen}" class="img-fluid">
        <div class="text-centered">Lorem Ipsum Dolor Sit Amen</div>
      </div>
      <div class="modal-footer">
        <button type="button" id="tempAddBtn" class="btn btn-primary" data-bs-dismiss="modal">Agregar al carrito.</button>
      </div>
    </div>
  </div>`);
  const modalCurrent = new bootstrap.Modal(document.getElementById('modalProducto'));
  const modCurrentEL = document.getElementById('modalProducto');
  modCurrentEL.addEventListener('show.bs.modal', event => {
    $('#tempAddBtn').click(function() {
        producto = productosTienda.find(producto => producto.id == id);
        actualizaCarro(producto);
    });
  });
  modCurrentEL.addEventListener('hidden.bs.modal', event => {
    $('#tempModal').remove();
  })  
  modalCurrent.show();
};

function viewCart(){
    $('#cuerpoTabla').empty();
    const totalQuantity = cart.reduce((accumulator, item) => accumulator + item.cantidad, 0);
        if (totalQuantity !=0) {
            cart.forEach((producto) => {
                $('#cuerpoTabla').append(`<tr><th scope = "row"><img src="${producto.imagen}" class="img-thumbnail"></img></th>
                <td>${producto.nombre}</td>
                <td>${producto.precio_total}</td>
                <td><input type="number" class="form-control" id="cantidadProducto" value="${producto.cantidad}"></td>
                <td><button id="deleteProducto" class="btn btn-danger"><i class="fa-solid fa-trash"></i></button></td>
              </tr>`);
        });
        const modalCarro = new bootstrap.Modal(document.getElementById('modalCarrito'));
       const modalCarroEL = document.getElementById('modalCarrito');
       modalCarroEL.addEventListener('hide.bs.modal', event => {
         indicadorCarro();
      });
       modalCarroEL.addEventListener('show.bs.modal', event => {
        $('#killCarroStorage').click(function(){
            localStorage.clear();
            modalCarro.hide();
        });
        $('#buttonCheckoOut').click(function(){
            window.location.replace('checkout.html');
        });
       });
       modalCarro.show();
    }   
}


$('#tablaCheckout').empty();
 const totalQuantity = cart.reduce((accumulator, item) => accumulator + item.cantidad, 0);
  if (totalQuantity !=0) {
            cart.forEach((producto) => {
                $('#tablaCheckout').append(`<tr><th scope = "row"><img src="${producto.imagen}" class="img-thumbnail"></img></th>
                <td>${producto.nombre}</td>
                <td>${producto.precio_total}</td>
                <td><input type="number" class="form-control" id="cantidadProducto" value="${producto.cantidad}"></td>
                <td><button id="deleteProducto" class="btn btn-danger"><i class="fa-solid fa-trash"></i></button></td>
              </tr>`);
        });
    }



//Selecciona todos los botones de la clase btn-primary dentro de un card-body. Luego, les añade
//un listener para ejecutar una función al hacer click´
 //Esto se asegurará de ejecutar este chunk de código solo en el index o galería
    $("button").each(function(){
        if($(this).parent().hasClass('card-body') && $(this).hasClass('btn-primary') ) {
        $(this).click(function() {
            const grandParent = $(this).parent().parent().attr('id');
            producto = productosTienda.find(producto => producto.id == grandParent);
            actualizaCarro(producto);
        });
    
        }});


//parecido a lo de arriba, pero con la clase btn-secondary
$("button").each(function(){
    if($(this).parent().hasClass('card-body') && $(this).hasClass('btn-secondary')) {
        $(this).click(function() {
            const grandParent = $(this).parent().parent().attr('id');
            viewElement(grandParent);
        });
    }
});

});


  



