import os
from flask import *  # lazy.
app = Flask(__name__)

LOGIN_COOKIE_NAME = 'is_logged_in'
STATIC_ROOT = 'static.imartinisisposano.it' if os.environ.get('SERVERTYPE') == 'AWS Lambda' or '127.0.0.1:8000/static'

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

    return render_template('index.html', static_root=STATIC_ROOT)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and request.form.get('password') == '1234':
        return set_cookie_and_redirect(request)

    return render_template('login.html', static_root=STATIC_ROOT)
