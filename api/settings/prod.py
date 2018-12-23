import dj_database_url
from urllib.parse import quote_plus

from .base import *


SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

# Hosts
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(';')
BASE_URL = os.environ.get('BASE_URL')

# EMAIL config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# Reservations settings
IS_ALWAYS_REVIEWABLE = False
