import os

from .settings_common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-vb_08&&o(0e9_o&#^ucukz091h6d0o7eiw01$0gsm&&v&kdmd5"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    os.environ['WEBSITE_HOSTNAME'] if 'WEBSITE_HOSTNAME' in os.environ else 'localhost'
]
