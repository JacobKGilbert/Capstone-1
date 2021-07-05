from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class LoginSignupForm(FlaskForm):
  '''Form for the login/signup process'''

  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class AddCartForm(FlaskForm):
  '''Form for adding product to cart.'''

  quantity = IntegerField('Qty', validators=[DataRequired(), NumberRange(min=1, max=20, message='Minimum quantity is 1. Maximum quantity is 20.')])

