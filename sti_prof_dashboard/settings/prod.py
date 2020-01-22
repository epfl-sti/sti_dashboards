import distutils.util
import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = distutils.util.strtobool(os.environ.get('DJANGO_DEBUG')) or False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DJANGO_POSTGRES_DB_NAME', 'sti_dashboards'),
        'USER': os.environ.get('DJANGO_POSTGRES_USERNAME', 'django'),
        'PASSWORD': os.environ.get('DJANGO_POSTGRES_PASSWORD', 'changeMe!'),
        'HOST': os.environ.get('DJANGO_POSTGRES_HOSTNAME', 'localhost'),
        'PORT': '',
    }
}

TABLEAU_BASE_URL = "https://tableau.epfl.ch/trusted/"

sentry_sdk.init(
    dsn="https://1845864e71354db2b404ad69b42279e1@sentry.io/1878562",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    environment="prod",
)
