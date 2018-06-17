import os
import random
import json

from models.rspv import DBManager

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


@app.route('/get_family', methods=['POST', ])
def get_family():
    dbman = DBManager()
    target = request.json['target']
    family = dbman.get_family(target)
    is_plus1 = False
    if family and len(family) == 1:
        if "p1_" in family[0]:
            is_plus1 = True
    return json.dumps({'family': family,'target': target,'is_plusone': is_plus1}), 200, {'ContentType': 'application/json'}


@app.route('/confirmation', methods=['POST', ])
def confirmation():
    dbman = DBManager()
    family = request.json['family']
    main_nome = request.json['main_nome']
    main_note = request.json['main_note']
    for member in family:
        #update target confirmation on db
        if 'is_plusone_of' in member.keys():
            dbman.set_confirmation(
                member['nome'],
                member['menu'],
                main_note if main_nome == member['nome'] else '',
                main_nome,
                member['is_plusone_of']
            )
        else:
            dbman.set_confirmation(
                member['nome'],
                member['menu'],
                main_note if main_nome == member['nome'] else '',
                main_nome,
                None
            )
    return json.dumps({'data': request.json, }), 200, {'ContentType': 'application/json'}


@app.route('/sample')
def sample():
    dbman = DBManager()
    target = '"hey": "ho"'
    family = dbman.get_family(target)
    is_plus1 = False
    if family and len(family) == 1:
        if "p1_" in family[0]:
            is_plus1 = True
    return json.dumps({'family': family,'target': target,'is_plusone': is_plus1}), 200, {'ContentType': 'application/json'}
