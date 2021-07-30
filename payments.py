from square.client import Client
from dotenv import load_dotenv
import os
import uuid

# Load environment variables from .env file
load_dotenv()

def make_payment(token, amount):
  # Create an instance of the API Client
  # and initialize it with the credentials
  # for the Square account whose assets you want to manage
  client = Client(
      access_token=os.environ.get('SQUARE_ACCESS_TOKEN'),
      environment='sandbox',
  )

  # Create an idempotency key to ensure no duplication of payments. Using uuid4 we ensure the randomness of the number while also ensuring the absolute privacy of the key.
  idempotency_key = str(uuid.uuid4())

  # Get an instance of the Square Payments API
  payments_api = client.payments

  body = {}
  body['source_id'] = token
  body['idempotency_key'] = idempotency_key
  body['amount_money'] = {}
  body['amount_money']['amount'] = amount
  body['amount_money']['currency'] = 'USD'
  body['location_id'] = os.environ.get('LOCATION_ID')

  result = payments_api.create_payment(body)

  if result.is_success():
    print(result.body)
  elif result.is_error():
    print(result.errors)
