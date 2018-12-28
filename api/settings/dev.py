import ptvsd
from .base import *


SECRET_KEY = 'z-+$tyr)mif-dsjx)vd#pkay86u_((ut^8(_0)283#bus5k&he'
DEBUG = True

# Hosts
ALLOWED_HOSTS = ['*']
BASE_URL = 'http://127.0.0.1:8000'


# CORS settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True


# CSRF & Session Domains
COOKIE_DOMAINS = {
    'http://dorm-portal.herokuapp.com': 'dorm-portal.herokuapp.com',
    'http://127.0.0.1:8000': '127.0.0.1',
    'http://127.0.0.1:8080': '127.0.0.1',
    'http://localhost:8080': '127.0.0.1'
}


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Languages
LANGUAGES = [
    ('en', 'English'),
    ('tr', 'Türkçe'),
    ('ar', 'العربية'),
]

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# run "python -m smtpd -n -c DebuggingServer localhost:1025"
EMAIL_HOST = 'localhost'

# Reservations settings
IS_ALWAYS_REVIEWABLE = True

# 5678 is the default attach port in the VS Code debug configurations
if False:
    print("Waiting for debugger attach")
    ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
    ptvsd.wait_for_attach()
