import json
from bottle import Bottle, route, static_file, template

app = Bottle()

with open('./static/settings.json', 'r') as jsf:
    settings = json.loads(jsf.read())
   
conference_name = settings['conference_name']
location = settings['location'] 


def skeleton(content_hook, hook='front'):
    return template(
        hook,
        content=content_hook,
        header=template('header')
    )


@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static')


@app.route('/')
def index():
    global conference_name
    return skeleton(template('index'), hook=conference_name)

"""
@app.route('/classifier/<hook>/')
def interface(hook):
    return skeleton(template('classifier', hook=hook.capitalize()))


@app.route('/classifier/<hook>/q?=<query>')
def classify(hook, query):
    return skeleton(template('query', hook=hook))
"""
