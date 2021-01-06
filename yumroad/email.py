import os
from flask import render_template
from yumroad.jobs import mailer

DOMAIN = os.getenv('MAILGUN_DOMAIN')
KEY = os.getenv('MAILGUN_KEY')
DEFAULT_FROM = f'Yumroad <yumroad@{DOMAIN}>'

def send_welcome_message(user):
    store = user.store
    subject = f"Welcome to Yumroad {store.name}"
    html_body = render_template('emails/welcome_pretty.html', store=store, preview_text='Here is how you get started with Yumroad.')
    mailer.send_email.queue(subject, [user.email], html_body, DOMAIN, KEY, DEFAULT_FROM, text_body=None, cc=None)

def send_purchase_email(email, product):
    store = product.store
    subject = f'Your purchase of {product.name} from {store.name}'
    html_body = render_template('emails/purchase.html', product=product)
    mailer.send_email.queue(subject, [email], html_body, DOMAIN, KEY, DEFAULT_FROM, text_body=None, cc=[store.user.email])