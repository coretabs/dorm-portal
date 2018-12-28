import dj_database_url
from urllib.parse import quote_plus

from .base import *


SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False


# Hosts
# ALLOWED_HOSTS sample env var: 'www.dorm-portal.com;.dorm-portal.com'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(';')
BASE_URL = os.environ.get('BASE_URL')


# CORS settings
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = False


# CSRF & Session Domains
# Sample env var: 'coretabs.net = .coretabs.net; 127.0.0.1 = 127.0.0.1'
COOKIE_DOMAINS = dict((host, target) for host, target in (a.split('=')
                                                          for a in os.environ.get('COOKIE_DOMAINS').split(';')))


# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}


# Languages
# Sample env var: 'en=English;tr=Turkce'
LANGUAGES = list((host, target) for host, target in (a.split('=')
                                                     for a in os.environ.get('LANGUAGES').split(';')))


# EMAIL config
"""
Sample env vars:
DEFAULT_FROM_EMAIL = Dorm Portal <no-reply@dorm-portal.com>
EMAIL_HOST = smtp.mailgun.org
EMAIL_HOST_PASSWORD = MySuperPassword
EMAIL_HOST_USER = no-reply@dorm-portal.com
"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Reservations settings
IS_ALWAYS_REVIEWABLE = False
