from flask import Blueprint, request, abort

from yumroad.extensions import csrf, checkout
from yumroad.email import send_purchase_email
from yumroad.models import Product

checkout_bp = Blueprint('checkout', __name__)

@checkout_bp.route('/webhooks/stripe', methods=['POST'])
@csrf.exempt  # Because this request is coming over an external API
def stripe_webhook():
    event = checkout.parse_webhook(request.data.decode("utf-8"), request.headers)
    if event.type == 'checkout.session.completed':
        # This is where we will we fulfill the order
        print(event['data'])
        session = event['data']['object']
        product_id = session['client_reference_id']
        product = Product.query.get(product_id)

        customer = checkout.get_customer(session['customer'])
        if not customer or not product:
            abort(400, 'Unknown product & customer')
        send_purchase_email(customer.email, product)

    return "OK", 200