https://developer.squareup.com/reference/square/payments-api
https://developer.squareup.com/docs/web-payments/take-card-payment
https://developer.squareup.com/reference/sdks/web/payments/card-payments

For this project I used the Square SDK and API for credit card processing. The main flow of the site is for a customer to select items from the catalog and add them to the cart. Then for the customer to be able to pay for the items in the cart. The database will then be updated from that submition. This involves reducing the on hand quantity of the item(s) purchased and adding the items to the orders_products database for cross referencing orders to products sold.

A few edits that will need to be made when time permits:
- The quantity needs to be included in the orders_products table to show how many of an item was sold.
- The "back end" for the business owner needs to be implemented.
  - This would involve an admin page for entering new items and seeing new orders that need to be shipped.
- Displaying, or emailing, the reciept the customer. (I was having issues with CORS to the Square receipt URL that is returned with the payment object.)
- Customer login and persistance for allowing customers to see their previous orders and potentially allow for easy reordering.