import os
import requests
import twilio.twiml
import re

from requests.auth import HTTPBasicAuth
from supporters_twilio.config import config_app
from flask import Flask, redirect, request, url_for, session

# Initialize the app
app = Flask('supporters_twilio')

# Set up the environment and logging
env = os.environ['ENV']
config_app(app, env)

try:
    API_URL = os.environ['GW_API_URL']
    API_CLIENT_ID = os.environ['GW_CLIENT_ID']
except KeyError:
    raise KeyError('You must set GW_API_URL, GW_CLIENT_ID environment variables.')

# The Twilio number is required, it's just used in the display.
try:
    TWILIO_NUMBER = os.environ['TWILIO_NUMBER']
except:
    TWILIO_NUMBER = 'your Twilio number'

class Supporter:
    bucket_url = API_URL + 'bucket'
    auth = HTTPBasicAuth(API_CLIENT_ID, '')

    def create(self, payload):
        req = requests.post(self.bucket_url, json=payload, auth=self.auth)
        print req.headers
        print req.status_code
        print req.text
        return req


@app.route('/', methods=['GET'])
def index():
    return '<h2 style="text-align:center;font-family:arial;">Text your email address to {}</h2>'.format(TWILIO_NUMBER)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    counter = session.get('counter', 0)
    counter += 1
    session['counter'] = counter
    body = request.values.get('Body', None)
    resp = twilio.twiml.Response()

    # First contact should contain an email address
    if counter == 1:
        session['email'] = body

        if not re.match(r'[^@]+@[^@]+\.[^@]+', body):
            message = 'Sorry, we couldn\'t find a valid email address in your message. Please try again.'
            session['counter'] = 0
            session['email'] = ''
            resp.message(message)
            return str(resp)
        else:
            message = 'Thanks for your interest in our mailing list. To confirm you want to join using {} reply to this message with \"YES\"'.format(body)
            resp.message(message)
            return str(resp)
    else:
        if re.search('YES', body, re.IGNORECASE):
            supporter = Supporter()
            payload = {
                'email': session.get('email'),
                'source': 'supporters-python-twilio-example',
                'tags': {
                    'email_template': 'signup_supporters_example'
                }
            }

            req = supporter.create(payload)
            if req.status_code == 201:
                session['counter'] = 0
                session['email'] = ''
                with resp.message('Thanks for Joining!') as m:
                    m.media(url_for('static', filename='images/confirm.jpg', _external=True))
                return str(resp)
            else:
                resp.message('We\'re having trouble signing you up, please reply with "YES" again.')
                return str(resp)
        else:
            session['counter'] = 0
            session['email'] = ''
            return ('', 204)


if __name__ == '__main__':
    app.run()
