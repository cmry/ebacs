import bottle
from .objects import Conference, Database

db = Database()


def post_get(name):
    """GET a POST (basically retrieves the info from a form)."""
    return bottle.request.forms.get(name)


def skeleton(hook, layout='front', var=None):
    """Wrapper to load templates."""
    return bottle.template(
        layout,
        content=hook,
        header=bottle.template('header', hook=Conference()),
        var=var
    )
