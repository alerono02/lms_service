import requests
from config.settings import STRIPE_API_KEY


def create_payment(payment_amount, currency='usd'):
    '''создание платежа'''
    headers = {'Authorization': f'Bearer {STRIPE_API_KEY}'}
    params = {'payment_amount': payment_amount, 'currency': currency}
    response = requests.post('https://api.stripe.com/v1/payment_intents', headers=headers, params=params)
    data = response.json()
    return data['id']


def retrieve_payment(id):
    '''получение платежа'''
    headers = {'Authorization': f'Bearer {STRIPE_API_KEY}'}
    response = requests.get(f'https://api.stripe.com/v1/payment_intents/{id}', headers=headers)
    return response.json()