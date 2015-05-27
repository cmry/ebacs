import bottle
from beaker.middleware import SessionMiddleware
from cork import Cork
from conf import *

session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'please use a random key and keep it secret!',
    'session.httponly': True,
    'session.timeout': 3600 * 24,
    'session.type': 'cookie',
    'session.validate_key': True,
}


app = SessionMiddleware(bottle.app(), session_opts)
user = User()
conf = Conference()
aaa = Cork('cork_conf', email_sender='c.emmery@outlook.com',
           smtp_url='smtp://smtp.magnet.ie')
authorize = aaa.make_auth_decorator(fail_redirect='/login', role="user")


def skeleton(content_hook, hook='front'):
    return bottle.template(
        hook,
        content=content_hook,
        header=bottle.template('header', hook=conf.name)
    )


@bottle.route('/static/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='static')


@bottle.route('/dash/')
def dashboard():
    pass


@bottle.route('/login')
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


@bottle.route('/')
def index():
    if not user.name:
        return skeleton(bottle.template('index'))
    else:
        return skeleton(bottle.template('dash'))

"""
@app.route('/classifier/<hook>/')
def interface(hook):
    return skeleton(template('classifier', hook=hook.capitalize()))


@app.route('/classifier/<hook>/q?=<query>')
def classify(hook, query):
    return skeleton(template('query', hook=hook))
"""


def main():

    # Start the Bottle webapp
    bottle.debug(True)
    bottle.run(app=app, host='localhost', port=8085,
               quiet=False, reloader=True)

if __name__ == "__main__":
    main()
