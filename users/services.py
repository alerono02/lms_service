import stripe

from config.settings import STRIPE_API_KEY

API_KEY = STRIPE_API_KEY


def get_session(payment):
    """ Функция возвращает сессию для оплаты """
    stripe.api_key = API_KEY

    product = stripe.Product.create(
        name=f'{payment.lesson if payment.lesson else payment.course}'
    )

    price = stripe.Price.create(
        currency='eur',
        unit_amount=int(payment.price)*100,
        product=f'{product.id}',
    )

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[
            {
                'price': f'{price.id}',
                'quantity': 1,
            }
        ],
        mode='payment',

    )
    return session.url
