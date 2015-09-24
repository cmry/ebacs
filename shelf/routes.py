import bottle
import subprocess
from os import chdir
from time import sleep
from .utils import db, skeleton, post_get
from .objects import settings, Submission


@bottle.route('/static/<filename>')
def server_static(filename):
    """For routing css files and images from the static folder."""
    return bottle.static_file(filename, root='static')


@bottle.get('/favicon.ico')
def get_favicon():
    """Seperate function to retrieve the favicon."""
    return server_static('favicon.ico')


@bottle.route('/')
def index():
    """Call the main page."""
    return skeleton(bottle.template('welcome'))


@bottle.route('/submit')
def show_submit():
    """Call the submission page."""
    return skeleton(bottle.template('submit_form'))


@bottle.post('/submit')
def submit():
    """Insert submission into db and parse it to XML."""
    reference_code = hash(post_get('title') +
                          str(post_get('authors')) +
                          settings['salt'])
    subm = Submission({
        'reference_code': reference_code,
        'name': post_get('name'),
        'title': post_get('title'),
        'authors': post_get('authors'),
        'affiliations': post_get('affils'),
        'contact': post_get('contact'),
        'site': post_get('site'),
        'text': post_get('text'),
        'references': post_get('ref'),
        'figurl': post_get('figurl'),
        'table': post_get('table'),
        'caption': post_get('caption')
    })
    db.save(subm)
    return skeleton(bottle.template('submit_message', var=reference_code))


def update(entry, reference_code):
    """After user edit, update the abstract."""
    db.save(entry)
    return skeleton(bottle.template('submit_message', var=reference_code))


def check_submission(reference_code):
    """Check if the submission is already completed."""
    try:
        q = db.search('subm', {'reference_code': int(reference_code)})
    except Exception:
        return None
    return q


@bottle.route('/view')
def check_code(var=None):
    """Ask for abstract code."""
    return skeleton(bottle.template('code_form', var=var))


@bottle.route('/compile')
def compile():
    """Compile the abstract (pretty ugly code here)."""
    entries, basedir = db.search('subm'), settings['basedir']
    with open(basedir + 'static/abstracts.xml', 'w') as xmlf:
        subm_str = ""
        i = 0
        for entry in entries:
            i += 1
            # TODO: accept a decision in the form, rather than this
            dummy_decision = 'presentation'  # or poster?
            subm_str += """
                        <submission id="%s">
                            <title>%s</title>
                            <keywords>
                                <keyword>submission</keyword>
                            </keywords>
                            <abstract>%s</abstract>
                            <decision>%s</decision>
                            <authors>
                        """ % (str(i), entry.title, entry.text,
                               dummy_decision)
            dummy_country = "Somewhere"
            for author, affil, contact in zip(entry.authors.split('; '),
                                              entry.affiliations.split('; '),
                                              entry.contact.split('; ')):
                author_l = author.split()
                author_first = author_l.pop(0)  # assumes only 1 first name
                author_second = ' '.join(author_l)
                if not author_second:
                    author_second = ''
                author_info = """
                                            <first_name> %s </first_name>
                                            <last_name> %s </last_name>
                                            <e-mail> %s </e-mail>
                                            <affiliation> %s </affiliation>
                                            <contact> %s </contact>
                            """ % (author_first, author_second, contact, affil,
                                   dummy_country)
                subm_str += """         <author>
                                            %s
                                        </author>
                        """ % author_info
            subm_str += """
                            </authors>
                        </submission>
                        """
        xmlf.write("""                   <submissions>  %s
                </submissions>
              """ % subm_str)
    # call ec2latex
    try:
        chdir(basedir + 'shelf')
        subprocess.call(['python2', 'ec2latex.py'])
        sleep(1)
        chdir(basedir + 'tex')
        subprocess.call(['pdflatex', 'bos_o.tex'])
        sleep(3)
        subprocess.call(['pdflatex', 'bos_o.tex'])
        sleep(3)
        chdir(basedir)
        subprocess.call(['mv', '-f', basedir + 'tex/bos_o.pdf',
                         basedir + 'static/'])
        return skeleton(bottle.template('book_form'))
    except KeyboardInterrupt:
        chdir(basedir)
        return skeleton(bottle.template('fail_form'))


@bottle.post('/view')
def view():
    """Load up the edit form without edit possiblities."""
    reference_code = post_get('reference_code')
    entry = check_submission(reference_code)
    if entry:
        return skeleton(bottle.template('edit_form', var=entry))
    else:
        return check_code(var="Sorry, your code seems invalid!")


@bottle.post('/edit')
def edit():
    """Load up the full blown edit form."""
    reference_code = post_get('reference_code')
    if reference_code:
        subm = check_submission(reference_code)
        db.delete(subm)
        new_subm = Submission({
            'reference_code': int(reference_code),
            'name': post_get('name'),
            'title': post_get('title'),
            'authors': post_get('authors'),
            'affiliations': post_get('affils'),
            'contact': post_get('contact'),
            'site': post_get('site'),
            'text': post_get('text'),
            'references': post_get('ref'),
            'figurl': post_get('figurl'),
            'table': post_get('table'),
            'caption': post_get('caption')
        })
        db.save(new_subm)
        return skeleton(bottle.template('submit_message', var=reference_code))
    else:
        return "Something went wrong..."
