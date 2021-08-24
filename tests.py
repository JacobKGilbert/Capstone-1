# run these tests like:
#
# python -m unittest tests.py

import os

# Set database url to the warbler-test database.
os.environ['DATABASE_URL'] = "postgresql:///ammo-surplus-test"

from models import db, connect_db, Product, Order, OrderProduct
from unittest import TestCase
from app import app
import payments

# Create all tables for tests.
db.create_all()

# Prevent WTForms from using CSRF and debug from intercepting redirects.
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['WTF_CSRF_ENABLED'] = False

PRODUCT_1 = {
  "price": 13.99,
  "caliber": "9mm",
  "grain": 115,
  "casing": "brass",
  "manufacturer": "Acme Ammo",
  "qty_per_box": 50,
  "box_qty_on_hand": 1000
}

PRODUCT_2 = {
  "price": 100,
  "caliber": "5.56",
  "grain": 62,
  "casing": "brass",
  "manufacturer": "AR Ammo",
  "qty_per_box": 1000,
  "box_qty_on_hand": 500
}

class AmmoSurplusTestCase(TestCase):
  '''Tests for views'''

  def setUp(self):
    '''Setup products'''
    Product.query.delete()

    product_1 = Product(**PRODUCT_1)
    product_2 = Product(**PRODUCT_2)

    db.session.add_all([product_1, product_2])
    db.session.commit()

    self.product_1 = product_1
    self.product_2 = product_2

  def tearDown(self):
    '''Clean up'''
    db.session.rollback()

  def test_home_view(self):
    with app.test_client() as client:
      resp = client.get("/")
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code, 200)
      self.assertIn('Acme Ammo', html)
      self.assertIn('AR Ammo', html)
      self.assertIn('<h5 class="card-title empty-cart-message">Oops... There\'s nothing in your cart.</h5>', html)

  
  def test_payment_route(self):
    with app.test_client() as client:
      json = {
          "token": "cnon:card-nonce-ok",
          "amount": 4197,  # Decimal moved two spaces due to Square API
          "products": '[{"ID": 'f'"{self.product_1.id}"'', "qty": "3"}]'
      }
      resp = client.post("/payment", json=json)

      self.assertEqual(resp.status_code, 200)

      prod_1 = Product.query.get(self.product_1.id)

      self.assertEqual(prod_1.box_qty_on_hand, 997)
