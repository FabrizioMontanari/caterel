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
        self.creds_dict = {
            "type": "service_account",
            "project_id": "martinisposi2018",
            "private_key_id": "a9a471ade108a900ddd476b042255a49cee88e71",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDLLqW1o94tAazC\nrteTVlc1U9Wc9A+ijdR6NhHkUDeLLvk6k/yjbzlAZrOX/Y/n6zYBIxXaqcG0RY1M\nLvE7n0/LzHDWDN6mfR3ilyqhAUH2gdIgksnDufZwMpoMscWYJJMRMRji6edfJ2/j\nwIQLfhDQrSNWaNrgYWW1a89pNdc+M7uGYSulMb66BqqViniW5uT4o2UR1dEGJbuz\ntEq8wiFTv0Rdz/SWMQWmfxc508Ah+OeGlp1IKuqu+YXRqBFeals0iHqob9iVOyso\nwDPmeNcJFF8y+QcnmSZrX7v3Nl8O3BE7EawLKbGsO4ycpgAKalMPBwPBAzs2knZ0\nXZIs5FKjAgMBAAECggEAAVFPH8ttQGt3XFfX7AuuSxk9FGR8yXgT/armGM3wXkWy\ntg+JnuG0xFcmKQEq8r0Sv5UjqiRZrjqZPPo89D8HPHIZ9TlmJDxBeluymhKxA9E5\ntJ5fEpbdI0Mgvp5UgrUSAxWHbMlJh9NwpVB1SsHJiCDnTsMlUDkxeKi3Up5Xw/58\n6x5kDDrqW8xth5yjfEpkVQKzYxxbdZDYWKh4488BmyaPImB6rVx2LoLX8iB0LCc1\n7nnpKWIvJMHINPh0MIkuljXRn5E61TbVsHQMme658YuF6wpjEgvgg2hq9L4gOPl3\nsWhddeulLUJGDKAFu2F6dPe7YkMermmsTFgw48OmyQKBgQD6701d4hohiBdYPLcV\nQPmiLXIOhothh3Gh22KwjfMhrkcZIG7MVneFNZJaWnVfqGDB0sr0ic/38ukIA+oE\npwaRlcDnoTKNa0kyKaahnMNsmo1dYJ5Wdml0R90wXLZwjV4Got2B34y5lBIpfc49\nGtrU6arTXkh1vsMKgfM28mqcHwKBgQDPSJXPzCZReIntuuhpZt3Tt+XN7GxtIcIC\nDNUv/+M6lRs8JOp2DHDkcrd0m6oX07drKVluI1eecNCp7KqtjQBTUqOIjkFE33Qj\nlwzjndc44BdK+B5jVHShGenuSvCXtOEHDjretEiUw4+Z/t/6tjXXBoa+i2Lco5GN\nqwsLJHb4/QKBgF6O/qB6K06nceSWPIeNzIQIjApdOPiviWpsuWu+kfgHLFOTnSzz\nCGbyIQxbOg+p64weWsx7ghr1NksG7pCCQD9sJx0h6WLRIuv8NgaAhEPQmaSuW/xI\n8sQWsIsg5L7VBrGJfd8K1oS3/4ATIDx2ei/xPaYYyUVVdTnobjYuc24RAoGBAIeU\nIHkkPMP5Ja5bHH0kjV9X33XLeDgBZpZUsnSM2KGOuZujQcAo7wZdimU5FA41qrjq\n+NWzRDIb9D/QzuppWZcmbFR7R3G2/o3w1LtkmEtZN6MPm0C5Evf0rS/x0GBKLQ2i\nXxsfrIGxUBIXxYSE/b5BRI0JOoa6bg/NmpGVLkQ5AoGBAINDmyEl+5mRe9xCTzJ8\nO7vINhC/0f4SMa1BG/SUvWxpWXWdizjgBz2Oxk7lkZGo1ZTehAN2Rl1au6NCrhM4\nMkK9pvC5k9JbPh112TryRyofxikigmd4uJkDjT96ih3dv8NCYt1y1KEd4399cpaz\n+WL+Woh+dbNkTsPiX1uNrn82\n-----END PRIVATE KEY-----\n",
            "client_email": "martinisposi@martinisposi2018.iam.gserviceaccount.com",
            "client_id": "104436276002869759452",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/martinisposi%40martinisposi2018.iam.gserviceaccount.com"
        }#non metto la chiave di accesso in pubblico!
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
    if family and len(family) == 1:
        if "p1_" in family[0]:
            is_plus1 = True
    return json.dumps({'family':family, 'target':target, 'is_plusone':is_plus1}), 200, {'ContentType':'application/json'}


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
    return json.dumps({'data':request.json,}), 200, {'ContentType':'application/json'} 
