import os
import random
import json

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
    dbman = DBManager()
    guest = ' '.join([
        request.args.get('nome', ''),
        request.args.get('cognome', '')
    ])

    return jsonify(dbman.get_family(guest))


@app.route('/confirmation', methods=['POST', ])
def confirmation():
    family_data = request.json.get('family')
    if type(family_data) != list:
        return 'Malformed Data', 400

    db_manager = DBManager()
    email_client = EmailClient()

    # TODO filter/clean
    db_manager.update_rsvp(family_data)
    # email_client.send_confirmation(family_data)

    # template_dictionary = {
    #     'guest_name': main_nome,
    #     'guest_email': main_email,
    #     'guest_note': main_note,
    #     'family': family
    # }

    # email_client.send_admin_notification(template_dictionary)
    # if main_email:
    #     email_client.send_guest_notification(
    #         to_email=main_email,
    #         template_dictionary=template_dictionary
    #     )


    return json.dumps({'data': request.json, }), 200, {'ContentType': 'application/json'}
