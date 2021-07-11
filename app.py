from flask import Flask, render_template, request
from models import db, connect_db
from forms import LoginSignupForm
from dotenv import load_dotenv
from flask_talisman import Talisman

import os

app = Flask(__name__)
Talisman(app)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///ammo_surplus'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

# load_dotenv()

connect_db(app)

@app.route('/')
def home():
    '''Get the home template.'''
    
    return render_template('cart.html')


# @app.route('/login', methods=['POST'])
# def login():
#     '''Handle Login'''
#     req = request.get_json()

#     form = ValidateForm(obj=req, meta={'csrf': False})
#     if request.method == 'POST' and form.validate():



# @app.route('/register', methods=['POST'])
# def register():
#     '''Handle registering new account.'''


