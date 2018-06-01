from flask import *  # lazy.
app = Flask(__name__)

LOGIN_COOKIE_NAME = 'is_logged_in'


@app.route('/')
def index():
    print('inhere')
    if 'km.' in request.host:
        base_host = request.host.replace('km.', '')
        res = make_response(redirect(f'https://{base_host}', 302))
        res.set_cookie(LOGIN_COOKIE_NAME, 'True', domain=f'{base_host}')
        return res

    is_logged_in = request.cookies.get(LOGIN_COOKIE_NAME)
    return f'Hello, World! logged in status is :{is_logged_in}:'


@app.route('/login')
def login():
    res = make_response('logged in!')
    res.set_cookie(LOGIN_COOKIE_NAME, 'True')
    return res
