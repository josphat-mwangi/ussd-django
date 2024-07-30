import os
from dotenv import load_dotenv

from ussd.settings.base import *

load_dotenv()

DEBUG = True

SECRET_KEY = os.getenv("SECRET_KEY")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# run on every host.
ALLOWED_HOSTS = ["*"]
