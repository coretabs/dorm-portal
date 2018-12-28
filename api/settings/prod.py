import dj_database_url
from urllib.parse import quote_plus

from .base import *


DEBUG = bool(os.environ.get('DEBUG'))
SECRET_KEY = os.environ.get('SECRET_KEY')

# Hosts
# ALLOWED_HOSTS sample env var: 'www.dorm-portal.com;.dorm-portal.com'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(';')
BASE_URL = os.environ.get('BASE_URL')


# CORS settings
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = False


# CSRF & Session Domains
# Sample env var: 'https://www.example.com=.example.com;https://example.com=.example.com'
try:
    COOKIE_DOMAINS = dict(
        (host, target) for host, target in (
            a.split('=') for a in os.environ.get('COOKIE_DOMAINS').split(';'))
    )
except:
    COOKIE_DOMAINS = {}


# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}


# Languages
# Sample env var: 'en=English;tr=Türkçe'
LANGUAGES = list((host, target) for host, target in (a.split('=')
                                                     for a in os.environ.get('LANGUAGES').split(';')))


# EMAIL config
"""
Sample env vars:
DEFAULT_FROM_EMAIL = Dorm Portal <no-reply@dorm-portal.com>
EMAIL_HOST = smtp.mailgun.org
EMAIL_HOST_USER = no-reply@dorm-portal.com
EMAIL_HOST_PASSWORD = MySuperPassword
"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Reservations settings
# Sample env var: 'false'
IS_ALWAYS_REVIEWABLE = bool(os.environ.get('IS_ALWAYS_REVIEWABLE'))
