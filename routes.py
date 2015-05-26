import json
from bottle import Bottle, route, static_file, template, request, response

app = Bottle()

with open('./static/settings.json', 'r') as jsf:
    settings = json.loads(jsf.read())

name = settings['conference_name']

username = None
password = None


def skeleton(content_hook, hook='front'):
    return template(
        hook,
        content=content_hook,
        header=template('header', hook=name)
    )


@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static')


@route('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        response.set_cookie("account", username, secret='some-secret-key')
        return template("<p>Welcome {{name}}! You are now logged in.</p>", name=username)
    else:
        return "<p>Login failed.</p>"


@app.route('/')
def index():
    if not username:
        return skeleton(template('index'))
    else:
        return skeleton(template('dashboard'))

"""
@app.route('/classifier/<hook>/')
def interface(hook):
    return skeleton(template('classifier', hook=hook.capitalize()))


@app.route('/classifier/<hook>/q?=<query>')
def classify(hook, query):
    return skeleton(template('query', hook=hook))
"""
