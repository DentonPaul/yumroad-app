from yumroad.extensions import rq2
import requests
import os

DOMAIN = os.getenv('MAILGUN_DOMAIN')
KEY = os.getenv('MAILGUN_KEY')
DEFAULT_FROM = f'Yumroad <yumroad@{DOMAIN}>'

@rq2.job
def send_email(subject, to_emails, html_body, DOMAIN, KEY, DEFAULT_FROM, text_body=None, cc=None, **kwargs):

    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", KEY),
        data = {
            "from": DEFAULT_FROM,
            "to": to_emails,
            "subject": subject,
            "html": html_body,
            "text": text_body,
            "cc": cc,
        }
    )