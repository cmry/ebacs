import bottle
from corks import aaa, authorize
from utils import skeleton
from objects import settings, Submission, Database

db = Database()


def post_get(name, default=''):
    return bottle.request.POST.get(name, default)


@bottle.route('/static/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='static')


@bottle.get('/favicon.ico')
def get_favicon():
    return server_static('favicon.ico')


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
def show_submit():
    return skeleton(bottle.template('submit_form'))


@bottle.post('/submit')
def submit():
    reference_code = hash(post_get('title') +
                          str(post_get('authors')) +
                          settings['salt'])
    db.save(Submission({
        'reference_code': reference_code,
        'title': post_get('title'),
        'authors': post_get('authors').split('; '),
        'affiliations': post_get('affils').split('; '),
        'contact': post_get('contact').split('; '),
        'text': post_get('text'),
        'references': post_get('ref'),
        'figurl': post_get('figurl'),
        'table': post_get('table'),
        'caption': post_get('caption')
        }))
    return skeleton(bottle.template('submit_message', var=reference_code))


# View submission
def check_submission(reference_code):
    print("I:", str(reference_code))
    return db.search('subm', {'reference_code': reference_code})


@bottle.route('/view')
def check_code(var=None):
    print("V")
    return skeleton(bottle.template('code_form', var=var))


@bottle.post('/view')
def view():
    reference_code = post_get('reference_code')
    if check_submission(reference_code):
        info = reference_code
        return skeleton(bottle.template('edit_form'), var=info)
    else:
        return check_code(var="Sorry, your code seems invalid!")


# Edit page

@bottle.route('/view/<id>')
@authorize(role="writer", fail_redirect="/sorry_page")
def edit():
    pass
