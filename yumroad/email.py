# from flask_mail import Message
# from yumroad.extensions import mail
import requests
import os
from flask import render_template

DOMAIN = os.getenv('MAILGUN_DOMAIN')
KEY = os.getenv('MAILGUN_KEY')
DEFAULT_FROM = f'Yumroad <yumroad@{DOMAIN}>'

def send_welcome_message(user):
    store = user.store

    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", KEY),
        data = {
            "from": DEFAULT_FROM,
            "to": [user.email],
            "subject": f"Welcome to Yumroad {store.name}",
            "html": render_template('emails/welcome_pretty.html', store=store, preview_text='Here is how you get started with Yumroad.')
        }
    )