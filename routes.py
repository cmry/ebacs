from bottle import Bottle, route, static_file, template, request, response
from conf import *

app = Bottle()
user = User()
conf = Conference()


def skeleton(content_hook, hook='front'):
    return template(
        hook,
        content=content_hook,
        header=template('header', hook=conf.name)
    )


@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static')


# Try BlitzDB as a local database thingy, would be SWEET if that worked.

@app.route('/dash/')
def dashboard():
    pass


@app.route('/login')
def do_login():
    # TODO: handle login with OAuth -- check cork
    # username = request.forms.get('username')
    # password = request.forms.get('password')
    # if check_login(username, password):
    #     response.set_cookie("account", username, secret='some-secret-key')
    #     return template("<p>Welcome {{name}}! You are now logged in.</p>",
    #                      name=username)
    # else:
    #     return "<p>Login failed.</p>"
    pass


@app.route('/')
def index():
    if not user.name:
        return skeleton(template('index'))
    else:
        return skeleton(template('dash'))

"""
@app.route('/classifier/<hook>/')
def interface(hook):
    return skeleton(template('classifier', hook=hook.capitalize()))


@app.route('/classifier/<hook>/q?=<query>')
def classify(hook, query):
    return skeleton(template('query', hook=hook))
"""
