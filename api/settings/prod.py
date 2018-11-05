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