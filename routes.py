import bottle
from corks import aaa, authorize
from utils import skeleton


@bottle.route('/static/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='static')


# Board page

@bottle.route('/')
@authorize()
def index():
    """Only authenticated users can see this"""
    # session = bottle.request.environ.get('beaker.session')
    # aaa.require(fail_redirect='/login')
    return 'Hi! <a href="/admin">Admin page</a> <a href="/logout">Logout</a>'


# Admin page

@bottle.route('/dash')
@authorize(role="admin", fail_redirect='/sorry_page')
@bottle.view('admin_page')
def admin():
    """Only admin users can see this"""
    # aaa.require(role='admin', fail_redirect='/sorry_page')
    return dict(
        current_user=aaa.current_user,
        users=aaa.list_users(),
        roles=aaa.list_roles()
    )


# Submission page

@bottle.route('/submit')
# @authorize(role="user", fail_redirect="/sorry_page")
def submit():
    return skeleton(bottle.template('submit_form'))