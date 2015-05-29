import bottle
from beaker.middleware import SessionMiddleware
from routes import *

session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'please use a random key and keep it secret!',
    'session.httponly': True,
    'session.timeout': 3600 * 24,
    'session.type': 'cookie',
    'session.validate_key': True,
}


app = SessionMiddleware(bottle.app(), session_opts)

def main():
    bottle.debug(True)
    bottle.run(app=app, host='localhost', port=8086,
               quiet=False, reloader=True)

if __name__ == "__main__":
    main()
