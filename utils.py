import bottle
from objects import Conference


def skeleton(hook, layout='front', var=None):
    return bottle.template(
        layout,
        content=hook,
        header=bottle.template('header', hook=Conference().name),
        var=var
    )
