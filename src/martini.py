import os
import random

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import datetime as dt

from flask import *  # lazy.
app = Flask(__name__)

LOGIN_COOKIE_NAME = 'is_logged_in'
STATIC_ROOT = '//static.imartinisisposano.it' if os.environ.get('SERVERTYPE') == 'AWS Lambda' else '//127.0.0.1:8000/static'

def set_cookie_and_redirect(request):
        base_host = request.host.replace('km.', '')
        res = make_response(redirect(f'http://{base_host}'))
        res.set_cookie(LOGIN_COOKIE_NAME, 'True', domain=f'{base_host}')
        return res




class DBManager(object):
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        #self.creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        self.creds_dict = {}#non metto la chiave di accesso in pubblico!
        self.creds = ServiceAccountCredentials.from_json_keyfile_dict(self.creds_dict, self.scope)
        self.client  = gspread.authorize(self.creds)

        self.sheet_family = self.client.open("MartiniWedding").worksheet("famiglie")
        self.sheet_confirmation = self.client.open("MartiniWedding").worksheet("conferme")

    def get_family(self, target):
        try:
            selected = self.sheet_family.find(target)
        except gspread.exceptions.CellNotFound as e:
            print(target, " non trovato")
            return None

        selected_family = self.sheet_family.row_values(selected.row)
        cleaned_family = [x for x in selected_family if x != target]
        return cleaned_family

    def set_confirmation(self, target, menu, notes, author, is_plusone_of):
        try:
            conf = self.sheet_confirmation.find(target) if is_plusone_of is None else self.sheet_confirmation.find("p1_" + is_plusone_of)
        except gspread.exceptions.CellNotFound as e:
            print(target, " non trovato per la conferma")
            return False
        # se +1 salvo anche il nome
        if is_plusone_of is not None:
            self.sheet_confirmation.update_cell(conf.row, conf.col, target)
            #TODO: aggiornare anche il foglio con le famiglie?????
            ref = self.sheet_family.find("p1_" + is_plusone_of)
            self.sheet_family.update_cell(ref.row, ref.col, target)

        self.sheet_confirmation.update_cell(conf.row, conf.col+1, menu)
        self.sheet_confirmation.update_cell(conf.row, conf.col+2, notes)
        self.sheet_confirmation.update_cell(conf.row, conf.col+3, author)
        self.sheet_confirmation.update_cell(conf.row, conf.col+4, dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
        # se +1 salvo il riferimento di quello che ha dato il +1
        if is_plusone_of is not None:
            self.sheet_confirmation.update_cell(conf.row, conf.col+5, is_plusone_of)
        return True





@app.route('/')
def index():
    if 'km.' in request.host:
        return set_cookie_and_redirect(request)

    if request.cookies.get(LOGIN_COOKIE_NAME) != 'True':
        return redirect('/login')

    return render_template(
        'index.html',
        static_root=STATIC_ROOT,
        background_version=random.randint(1,2)
    )


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and request.form.get('password').lower() == 'ellie':
        return set_cookie_and_redirect(request)

    return render_template('login.html', static_root=STATIC_ROOT)


@app.route('/get_family', methods=['POST',])
def get_family():
    dbman = DBManager()
    target = request.json['target']
    family = dbman.get_family(target)
    is_plus1 = False
    if len(family) == 1:
        if "p1_" in family[0]:
            is_plus1 = True
    return json.dumps({'success':True, 'family':family, 'target':target, 'is_plusone':is_plus1}), 200, {'ContentType':'application/json'}


@app.route('/confirmation',methods=['POST',])
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
    return json.dumps({'success':True, 'data':request.json,}), 200, {'ContentType':'application/json'} 
