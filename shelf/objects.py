import json
from blitzdb import Document, FileBackend

with open('./static/settings.json', 'r') as jsf:
    settings = json.loads(jsf.read())


class Conference:

    """Stores environment variables taken from settings.json."""

    def __init__(self):
        """Set attributes."""
        self.name = settings['conference_name']
        self.lead = settings['conference_subtitle']
        self.location = settings['location']

class Submission(Document):

    """Empty class used for blitzdb."""

    pass


class User(Document):

    """Empty class used for blitzdb."""

    pass


class Database:

    """Blitzdb database object."""

    def __init__(self):
        """Loads the database, location could be somewhere else."""
        self.backend = FileBackend(settings['database_location'])

    def save(self, entry):
        """Save some entry to the database."""
        self.backend.save(entry)
        self.backend.commit()

    def delete(self, entry):
        """Delete some entry from the database."""
        self.backend.delete(entry)
        self.backend.commit()

    def search(self, table, query=None):
        """Search for query in the associated table."""
        if table == 'user':
            doc = User
        elif table == 'subm':
            doc = Submission
        try:
            if query:
                return self.backend.get(doc, query)
            else:
                return self.backend.filter(doc, {})
        # not sure if this works?
        except doc.DoesNotExist:
            return None
