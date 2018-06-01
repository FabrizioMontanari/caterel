from flask import *  # lazy.
app = Flask(__name__)


BASE_URL = 'test.imartinisisposano.it'


@app.route('/')
def index():
    print(request.host)
    if request.host == f'km.{BASE_URL}':
        res = make_response(redirect(f'http://{BASE_URL}', 302))
        res.set_cookie('is_logged_in', 'True', domain=f'{BASE_URL}')
        return res

    is_logged_in = request.cookies.get('is_logged_in')
    return f'Hello, World! {is_logged_in}'


@app.route('/login')
def login():
    res = make_response('logged in!')
    res.set_cookie('is_logged_in', 'True')
    return res


@app.route('/logout')
def logout():
    res = make_response('logged out!')
    res.set_cookie('is_logged_in', expires=0)
    return res
