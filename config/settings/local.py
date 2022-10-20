import socket

from config.settings.base import *

DEBUG = True
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2", '0.0.0.0']
ALLOWED_HOSTS = INTERNAL_IPS
INSTALLED_APPS += [
    'django_createsuperuserwithpassword',
    'debug_toolbar',
]
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
