from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.email}>"

    @classmethod
    def signup(cls, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Product(db.Model):
    '''Products'''

    __tablename__ = 'products'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    caliber = db.Column(
        db.Text,
        nullable=False
    )

    grain = db.Column(
        db.Integer,
        nullable=False
    )

    bullet = db.Column(
        db.Text,
        nullable=False
    )

    casing = db.Column(
        db.Text,
        nullable=False
    )

    manufacturer = db.Column(
        db.Text,
        nullable=False
    )

    qty_per_box = db.Column(
        db.Integer,
        nullable=False
    )

    box_qty_on_hand = db.Column(
        db.Integer,
        nullable=False
    )

class Order(db.Model):
    '''Orders'''

    __tablename__ = 'orders'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user = db.relationship('User', backref='orders')

    products = db.relationship('Product', secondary='orders_products')

class OrderProduct(db.Model):
    '''Orders to Products'''

    __tablename__ = 'orders_products'

    order_id = db.Column(
        db.Integer,
        db.ForeignKey('orders.id', ondelete='cascade'),
        nullable=False,
        primary_key=True
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id', ondelete='cascade'),
        nullable=False,
        primary_key=True
    )

def connect_db(app):
    """Connect this database to provided Flask app.

      Called in Flask app.
    """

    db.app = app
    db.init_app(app)
