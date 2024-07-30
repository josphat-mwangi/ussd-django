import os
import dj_database_url
from ussd.settings.base import *


ADMINS = (("Josphat Mwangi", "josphatwanjiruw@gmail.com"))

# always set this to false in production
DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']


# restrict it to only your domain
ALLOWED_HOSTS = ['*']

DATABASES = {}
DATABASES["default"] = dj_database_url.config(
    conn_max_age=600, ssl_require=True)


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_PASSWORD"]

EMAIL_PORT = 587
EMAIL_USE_TLS = True
