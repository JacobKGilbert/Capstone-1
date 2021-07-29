/* Cart Functionality */

/** Adjusts total price due based on current cart items. */ 
function changeTotalPayment() {
  let totalElement = $('#amount-total')
  let subTotals = $('.subtotal')
  let totalAmount = 0

  for (const subtotal of subTotals) {
    let subT = parseFloat($(subtotal).text())

    totalAmount += subT
  }

  totalElement.text(totalAmount)
  if (totalAmount === 0) {
    $('.empty-cart-message').show()
  }
}

function showOrHideProductFromCatalog(product) {
  $(product).toggle()
}

function removeProductFromCart(cartProduct) {
  $(cartProduct).remove()
}

/** Adjusts the quantity and subtotal of the input and subtotal span, respectively. Then calls changeTotalPayment */
function updateCart(productID, quantity, price) {
  let cartFormInput = $(`#qty-${productID}`)
  let cartItemSubtotal = $(`#product${productID}-subtotal`)

  cartFormInput.val(quantity)

  let subtotal = quantity * price
  cartItemSubtotal.text(`${subtotal}`)

  changeTotalPayment()
}

/** Creates cart item and adds it to cart. Also adds submit trigger to created item's form. */
function addProductToCart(productID, quantity, price) {
  let title = $(`#product-id${productID}`).text()
  let subtotal = quantity * price

  // Create cart item
  let cartItem = $(`
      <div id='item-id${productID}'>
        <p class='card-text'>${title}</p>
        <div class="row g-0">
          <div class="col-md-8">
            <form class='cart-item-form' id='${productID}'>
              <div class='input-group input-group-sm mb-4'>
                <label for='quantity' class='col-sm-3 col-form-label col-form-label-sm hidden'>Qty</label>
                <input type='number' name='quantity' class='quantity form-control col-sm-4' id='qty-${productID}' max='10' min='0' value='${quantity}'
                  required>
                <button type='submit' class='btn btn-outline-secondary edit-qty-btn'>Update</button>
              </div>
            </form>
          </div>
          <div class='col-md-4'>
            <p class='align-middle'>$<span class='subtotal' id='product${productID}-subtotal'>${subtotal}</span></p>
          </div>
        </div>
        <hr>
      </div>
    `)

  $('#cart-divider').after(cartItem)

  changeTotalPayment()

  /**  Submit trigger on the product card in cart to remove from cart and add to catalog if quantity is reduced to zero. Else it will call updateCart*/
  $(`#item-id${productID} form`).submit(function (evt) {
    evt.preventDefault()

    let form = evt.currentTarget
    let input = form[0]
    let productID = $(form).attr('id')
    let quantity = parseFloat($(input).val())
    let price = parseFloat($(`#product-price${productID}`).text())
    let cartProduct = form.closest(`#item-id${productID}`)
    let catalogProduct = $(`#product${productID}div`)

    if (quantity > 0) {
      updateCart(productID, quantity, price)
    } else {
      showOrHideProductFromCatalog(catalogProduct)
      removeProductFromCart(cartProduct)
      changeTotalPayment()
    }
  })
}

// Submit trigger on the product card in catalog to add selected product to cart and remove same from catalog list
$('.product-form').submit(function (evt) {
  evt.preventDefault()

  let form = evt.currentTarget
  let input = form[0]
  let productID = $(form).attr('id')
  let quantity = parseFloat($(input).val())
  let price = parseFloat($(`#product-price${productID}`).text())
  let product = form.closest('.col')

  $('.empty-cart-message').hide()
  addProductToCart(productID, quantity, price)
  $(form)[0].reset()
  showOrHideProductFromCatalog(product)
})