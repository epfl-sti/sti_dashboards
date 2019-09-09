from django.contrib.auth.models import AbstractUser
from django.db import models
from url_or_relative_url_field.fields import URLOrRelativeURLField


class Person(AbstractUser):
    sciper = models.IntegerField(null=True, blank=True, default=None)
    is_dean = models.BooleanField(null=False, blank=False, default=False)
    is_institute_manager = models.BooleanField(null=False, blank=False, default=False)
    picture_url = URLOrRelativeURLField(blank=True, null=True, default=None)

# objects not existing in the database


class NextStep(object):
    def __init__(self, title=None, description=None, link=None):
        self.title = title
        self.description = description
        self.link = link
