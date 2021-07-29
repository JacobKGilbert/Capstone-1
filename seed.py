"""Seed database with sample data from CSV Files."""

from csv import DictReader
from app import app, db
# To add login/signup functionality import User (uncommented in models)
from models import Product, Order, OrderProduct

db.drop_all()
db.create_all()

with open('generator/products.csv') as products:
    db.session.bulk_insert_mappings(Product, DictReader(products))

db.session.commit()