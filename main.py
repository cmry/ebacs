import json
from routes import app
from bottle import run, default_app

default_app.push(app)

# run()
run(app=app, host='localhost', port=8085)
