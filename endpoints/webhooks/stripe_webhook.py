import stripe
from flask import request, jsonify

from configs.config import settings
from integrations.stripe_methods import add_from_stripe, delete_from_stripe, update_from_stripe


def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.get('ENDPOINT_SECRET')
        )
    except ValueError as e:
        raise e
    except stripe.error.SignatureVerificationError as e:
        raise e

    if event['type'] == 'customer.created':
        customer = event['data']['object']
        add_from_stripe(customer)

    elif event['type'] == 'customer.deleted':
        customer = event['data']['object']
        delete_from_stripe(customer)

    elif event['type'] == 'customer.updated':
        customer = event['data']['object']
        update_from_stripe(customer)

    else:
        print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)


