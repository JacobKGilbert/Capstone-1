from flask import Flask, render_template, redirect, request, flash, session, g, url_for
# To add login/signup functionality import User (uncomment in models)
from models import db, connect_db, Product, Order, OrderProduct
# from forms import LoginSignupForm
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from payments import make_payment
import json

import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///ammo_surplus'))
# Heroku uses 'postgres' while sqlalchemy (version 1.4) only allows 'postgresql'
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace(
        "postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "Acts2:38")

load_dotenv()

connect_db(app)

# Helper Functions

def get_products_from_db(products):
    res = []

    for product in products:
        found_product = Product.query.filter_by(id=product['ID']).first()
        res.append(found_product)
        quantity = int(product['qty'])
        found_product.box_qty_on_hand -= quantity
        db.session.add(found_product)
    
    return res

def update_order_products_table(q_products):
    order = Order(products=q_products)
    db.session.add(order)

# CURR_USER = 'current user'

# @app.before_request
# def add_user_to_g():
#     """If we're logged in, add curr user to Flask global."""

#     if CURR_USER in session:
#         g.user = User.query.get(session[CURR_USER])

#     else:
#         g.user = None


# def do_login(user):
#     """Log in user."""

#     session[CURR_USER] = user.id


# def do_logout():
#     """Logout user."""

#     if CURR_USER in session:
#         del session[CURR_USER]


@app.route('/')
def home():
    '''Get the home template.'''
    products = Product.query.order_by(Product.id).all()
    APPLICATION_ID = os.environ.get('APPLICATION_ID')
    LOCATION_ID = os.environ.get('LOCATION_ID')

    return render_template('home.html', products=products, APPLICATION_ID=APPLICATION_ID, LOCATION_ID=LOCATION_ID)


# @app.route('/login', methods=['POST'])
# def login():
#     '''Handle Login'''
#     req = request.get_json()

#     form = LoginSignupForm(obj=req, meta={'csrf': False})
#     if request.method == 'POST' and form.validate():
#         user = User.authenticate(form.email.data,
#                                  form.password.data)

#         if user:
#             do_login(user)
#             flash(f"Welcome!", "success")
#             return redirect("/")

#         flash("Invalid credentials.", 'danger')
    
#     return redirect('/')

# @app.route('/register', methods=['POST'])
# def register():
#     '''Handle registering new account.'''
#     req = request.get_json()

#     form = LoginSignupForm(obj=req, meta={'csrf': False})
#     if request.method == 'POST' and form.validate():
#         try:
#             user = User.signup(
#                 email=form.email.data,
#                 password=form.password.data
#             )
#             db.session.commit()

#         except IntegrityError:
#             flash("Email already taken", 'danger')
#             return render_template('cart.html')

#         do_login(user)

#         return redirect("/")

@app.route('/payment', methods=['POST'])
def payment():
    req = request.get_json()
    token = req['token']
    amount = int(req['amount'])
    products_in_cart = req['products']
    products = json.loads(products_in_cart)

    # Collect products from db and update the orders_products table.
    q_products = get_products_from_db(products)
    update_order_products_table(q_products)
    
    db.session.commit()

    res = make_payment(token, amount)
    return res.body

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
