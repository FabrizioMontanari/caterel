import os
import random
import json
import traceback

from models.db_manager import DBManager
from models.email_client import EmailClient

from flask import *  # lazy.
app = Flask(__name__)


STATIC_ROOT_NAMES = {
    'local': '//127.0.0.1:8000/static',
    'dev': '//s3-eu-west-1.amazonaws.com/www.imartinisisposano.it/static/dev',
    'prod': '//static.imartinisisposano.it'
}

STAGE_NAME = os.environ.get('STAGE', default='local')
STATIC_ROOT = STATIC_ROOT_NAMES[STAGE_NAME]
LOGIN_COOKIE_NAME = 'is_logged_in'


def set_cookie_and_redirect(request):
    base_host = request.host.replace('km.', '')
    res = make_response(redirect(f'http://{base_host}'))
    res.set_cookie(LOGIN_COOKIE_NAME, 'True', domain=f'{base_host}')
    return res


@app.route('/')
def index():
    if 'km.' in request.host:
        return set_cookie_and_redirect(request)

    if request.cookies.get(LOGIN_COOKIE_NAME) != 'True':
        return redirect('/login')

    return render_template(
        'index.html',
        static_root=STATIC_ROOT,
        background_version=random.randint(1, 2)
    )


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and request.form.get('password').lower() == 'ellie':
        return set_cookie_and_redirect(request)

    return render_template(
        'login.html',
        static_root=STATIC_ROOT
    )


@app.route('/get_family')
def get_family():
    try:
        guest_data = request.args.get('guestFullName')

        db_manager = DBManager()
        guest_data = db_manager.get_family(guest_data)
        
        return jsonify(guest_data)
    except:
        # dump trace and request to cloudwatch and recover.
        traceback.print_exc()
        print(request.json)
        
        return json.dumps({'received_request': request.json, 'status': 'Server Error' }), 500 , {'ContentType': 'application/json'}




@app.route('/confirmation', methods=['POST', ])
def confirmation():
    try:
        family_data = request.json.get('family')

        db_manager = DBManager()
        db_manager.update_rsvp(family_data)

        email_client = EmailClient()
        email_client.send_rsvp_notifications(family_data)

        return 'Success', 200
    except:
        # dump trace and request to cloudwatch and recover.
        traceback.print_exc()
        print(request.json)
        
        return json.dumps({'received_request': request.json, 'status': 'Server Error' }), 500 , {'ContentType': 'application/json'}

