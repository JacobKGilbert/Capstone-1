## Stack
Frontend: Javascript/JQuery

Backend: Flask/Python/PostgreSQL

Other Requirements: Sqlalchemy/WTForms/Bcrypt

## How does it work?
The main flow of the site is for a customer to select items from the catalog and add them to the cart. Then for the customer to be able to pay for the items in the cart. The database will then be updated from that submission. This involves reducing the on hand quantity of the item(s) purchased and adding the items to the orders_products database for cross referencing orders to products sold.

For this project I used the Square SDK and API for credit card processing.

https://developer.squareup.com/reference/square/payments-api

https://developer.squareup.com/docs/web-payments/take-card-payment

https://developer.squareup.com/reference/sdks/web/payments/card-payments

## How to install locally.
1. Clone a copy of this repo to your machine.
2. Install Python 3.7.x (If you don't have it already.)
3. Navigate into the project folder/directory
4. Set up virtual environment within this directory.
```
python3 -m venv venv
source venv/bin/activate
```
5. Install all requirements within the virtual environment.
```
pip install -r requirements.txt
```
6. Install PostgreSQL (If you don't have it already.)
7. Setup local database.
```
createdb ammo_surplus
```
8. Run seed file in ipython
```
ipython

%run seed.py
```
9. Start the server.
```
python app.py
```
10. Navigate to the localhost address that is displayed. (i.e. https://127.0.0.1:5000/)
     - Notice that this is running through HTTPS. This is because the Square SDK does not allow processing through HTTP. This is achieved by using an adhoc certificate (see last line of app.py). You will need to ignore the warning that is raised when first starting the server. You will only have to do ignore this warning again if you restart the server or edit anything that restarts the server. Please see the following blog post for more information on how this works. https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

## How to run tests.
1. Create test database.
```
createdb ammo-surplus-test
```
2. Run tests
```
python -m unittest tests.py
```

## Future Features
A few edits that will need to be made when time permits:
- The quantity needs to be included in the orders_products table to show how many of an item were sold.
- The "back end" for the business owner needs to be implemented.
  - Admin page for entering new items 
  - Seeing new orders that need to be shipped.
- Displaying, or emailing, the receipt to the customer. (I was having issues with CORS to the Square receipt URL that is returned with the payment object.)
- Customer login and persistance for allowing customers to see their previous orders and potentially allow for easy reordering.