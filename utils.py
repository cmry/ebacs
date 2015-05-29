import bottle
from objects import Conference, Database


class Texparse:

	def __init__(self, subm):
		"""
		subm : class
			The class subm is defined in objects.Submission and has the 
			following fields as attributes:
				- reference_code 	- title  	- authors  	- affils
				- contact 			- text 		- ref 		- figurl
				- table 			- caption
		"""

		self.subm = subm



tex = Texparse()
db = Database()


def post_get(name, default=''):
    return bottle.request.forms.get(name)


def skeleton(hook, layout='front', var=None):
    return bottle.template(
        layout,
        content=hook,
        header=bottle.template('header', hook=Conference()),
        var=var
    )
