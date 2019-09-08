from django.db import models

####### objects not existing in the database
class NextStep(object):
    def __init__(self, title=None, description=None, link=None):
        self.title = title
        self.description = description
        self.link = link
