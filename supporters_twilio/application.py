import os
import requests
import twilio.twiml

from requests.auth import HTTPBasicAuth
from supporters_twilio.config import config_app
from flask import Flask, redirect, request, url_for, render_template

# Initialize the app
app = Flask('supporters_twilio')

# Set up the environment and logging
env = os.environ['ENV']
config_app(app, env)

try:
    API_URL = os.environ['GW_API_URL']
    API_CLIENT_ID = os.environ['GW_CLIENT_ID']
except KeyError:
    raise KeyError('You must set GW_API_URL and GW_CLIENT_ID environment variables.')

class Supporter:
    bucket_url = API_URL + 'bucket'
    auth = HTTPBasicAuth(API_CLIENT_ID, '')

    def create(self, payload):
        req = requests.post(self.bucket_url, json=payload, auth=self.auth)
        print req.headers
        print req.status_code
        print req.text
        return req

#
# @app.route('/success/')
# def success():
#     return render_template(
#         'success.html',
#         email=request.args.get('email')
#     )

@app.route('/', methods=['GET', 'POST'])
def hello():
    resp = twilio.twiml.Response()
    resp.message('hi, robot')
    return str(resp)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     error = False
#     errorMsg = False
#     supporter = Supporter()
#
#     if request.method == 'POST':
#         payload = {
#             'givenName': request.form['givenName'],
#             'email': request.form['email'],
#             'source': request.form['source'],
#             'tags': {
#                 'email_template': 'signup_supporters_example'
#             }
#         }
#
#         if not payload['givenName'] or not payload['email']:
#             error = True
#             errorMsg = 'We need both your name and email to sign you up.'
#         else:
#             req = supporter.create(payload)
#
#             if req.status_code == 201:
#                 return redirect(url_for('success', email=payload['email']))
#             else:
#                 error = True
#
#     return render_template(
#         'sign_up.html',
#         errorMsg=errorMsg,
#         error=error
#     )

if __name__ == '__main__':
    app.run()
