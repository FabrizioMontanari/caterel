from flask import *  # lazy.
app = Flask(__name__)

LOGIN_COOKIE_NAME = 'is_logged_in'

def set_cookie_and_redirect(request):
        base_host = request.host.replace('km.', '')
        res = make_response(redirect(f'http://{base_host}', 302))
        res.set_cookie(LOGIN_COOKIE_NAME, 'True', domain=f'{base_host}')
        return res


@app.route('/')
def index():
    if 'km.' in request.host:
        return set_cookie_and_redirect(request)

    is_logged_in = request.cookies.get(LOGIN_COOKIE_NAME)
    return f'Hello, World! logged in status is :{is_logged_in}:'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and request.form['password'] == '1234':
        return set_cookie_and_redirect(request)

    return render_template('login.html')
