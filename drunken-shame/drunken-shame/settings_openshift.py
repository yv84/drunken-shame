# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

"""
[Openshift] Django project settings.
"""

import os
from .settings import *
from unipath import FSPath as Path

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE'    : 'django.db.backends.postgresql_psycopg2',
        'NAME'      : os.environ['OPENSHIFT_APP_NAME'],
        'USER'      : os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
        'PASSWORD'  : os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
        'HOST'      : os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
        'PORT'      : os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
        }
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = Path(os.environ['OPENSHIFT_DATA_DIR']).child('site_media')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = Path(os.environ['OPENSHIFT_DATA_DIR']).child('site_static')

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

STATICFILES_STORAGE = 'drunken-shame.s3utils.StaticRootS3BotoStorage'

# add your own custom settings here

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    os.environ['OPENSHIFT_GEAR_DNS'],
    # 'http://your.custom.domain.com
]

# Make this unique, and don't share it with anybody.
# SECRET_KEY = os.environ['SECRET_KEY']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
            },
        }
}
