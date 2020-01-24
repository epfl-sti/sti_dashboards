import os

from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

INTERNAL_IPS = ['127.0.0.1', ]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

INSTALLED_APPS += ['debug_toolbar', ]

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

TABLEAU_BASE_URL = "https://tableau-tst.epfl.ch/trusted/"

PEOPLE_WS_ENDPOINT = 'https://test-people.epfl.ch/cgi-bin/wsgetpeople?scipers={}'
