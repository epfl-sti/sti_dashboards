from django.contrib.auth.models import AbstractUser
from django.db import models


class Person(AbstractUser):
    sciper = models.IntegerField(null=True, blank=True, default=None)

# objects not existing in the database


class NextStep(object):
    def __init__(self, title=None, description=None, link=None):
        self.title = title
        self.description = description
        self.link = link
