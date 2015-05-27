import bottle
from objects import Conference


def skeleton(content_hook, hook='front'):
    return bottle.template(
        hook,
        content=content_hook,
        header=bottle.template('header', hook=Conference().name)
    )
