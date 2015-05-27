import json
# from blitzdb import Document, FileBackend

with open('./static/settings.json', 'r') as jsf:
    settings = json.loads(jsf.read())


class Conference:

    def __init__(self):
        self.name = settings['conference_name']
        self.location = settings['location']

    def func():
        pass


class Submission():
    def __init__(self):
        self.authors = None
        self.pdf = None

    def func():
        pass


class User():

    def __init__(self):
        self.name = None
        self.password = None

    def func():
        pass


# class Database:

#     def __init__(self):
#         self.backend = FileBackend(settings['database_location'])

#     def save(self, entry):
#         self.backend.save(entry)
#         self.backend.commit()
