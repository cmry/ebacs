import bottle
from objects import Conference, Database

db = Database()


def post_get(name, default=''):
    return bottle.request.forms.get(name)


def skeleton(hook, layout='front', var=None):
    return bottle.template(
        layout,
        content=hook,
        header=bottle.template('header', hook=Conference().name),
        var=var
    )
