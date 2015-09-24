import os, sys

os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))

import bottle
from beaker.middleware import SessionMiddleware
from shelf.routes import *

session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'please use a random key and keep it secret!',
    'session.httponly': True,
    'session.timeout': 3600 * 24,
    'session.type': 'cookie',
    'session.validate_key': True,
}


application = SessionMiddleware(bottle.app(), session_opts)

def main():
    bottle.debug(True)
    bottle.run(app=application, host='localhost', port=8086,
               quiet=False, reloader=True)

if __name__ == "__main__":
    main()
