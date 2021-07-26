function removeProductFromCatalog(product) {
  $(product).hide()
}

function addProductToCart(productID, quantity, price) {
  title = $(`#product-id${productID}`).text()
  cart = $('#cart-body')
  totalElement = $('#amount-total')

  subTotal = quantity * price
  
  totalAmount = parseFloat(totalElement.text())
  newTotal = totalAmount + subTotal

  totalElement.text(newTotal)

  // Create cart item
  cartItem = $(`
      <div id='item-id${productID}'>
      <p class='card-text'>${title}</p>
      <div class="row g-0">
        <div class="col-md-8">
          <form action='#' class='cart-item-form' id='${productID}'>
            <div class='input-group input-group-sm mb-4'>
              <label for='quantity' class='col-sm-3 col-form-label col-form-label-sm hidden'>Qty</label>
              <input type='number' name='quantity' class='quantity form-control col-sm-4' max='10' min='0' value='${quantity}'
                required>
              <button type='submit' class='btn btn-outline-secondary edit-qty-btn'>Update</button>
            </div>
          </form>
        </div>
        <div class="col-md-4">
          <p class="align-middle">$${subTotal}</p>
        </div>
      </div>
      <hr>
      </div>
    `)

  $('#cart-divider').after(cartItem)
}

function removeProductFromCart(product) {
  
}

function addProductToCatalog(product) {
  $(product).show()
}

// Submit trigger to add selected product to cart and remove same from catalog list
$('.product-form').submit(function (evt) {
  evt.preventDefault()

  $('.empty-cart-message').remove()

  form = evt.currentTarget
  input = form[0]
  productID = $(form).attr('id')
  quantity = parseFloat($(input).val())
  price = parseFloat($(`#product-price${productID}`).text())

  addProductToCart(productID, quantity, price)

  product = form.closest('.col')

  removeProductFromCatalog(product)
})