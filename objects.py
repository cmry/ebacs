import json
from blitzdb import Document, FileBackend

with open('./static/settings.json', 'r') as jsf:
    settings = json.loads(jsf.read())


class Conference:

    def __init__(self):
        self.name = settings['conference_name']
        self.lead = settings['conference_subtitle']
        self.location = settings['location']

    def func():
        pass


class Submission(Document):
    pass


class User(Document):
    pass


class Database:

    def __init__(self):
        self.backend = FileBackend(settings['database_location'])

    def save(self, entry):
        self.backend.save(entry)
        self.backend.commit()

    def search(self, table, query):
        if table == 'user':
            doc = User
        elif table == 'subm':
            doc = Submission
        try:
            return self.backend.get(doc, query)
        except doc.DoesNotExist:
            return None
