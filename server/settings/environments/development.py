"""
Development environment settings for Django Project.

These settings are specific to the development environment.
"""

import socket

from server.settings.components import config
from server.settings.components.common import INSTALLED_APPS, MIDDLEWARE
from server.settings.components.database import DATABASES


SECRET_KEY = config("DJANGO_SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = [
    f'*.{config("DOMAIN_NAME")}',
    config("DOMAIN_NAME"),
    config("DOMAIN_IP"),
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "[::1]",
]


# Django Debug Toolbar
# For more information see the documentation:
# https://django-debug-toolbar.readthedocs.io/en/latest/

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

# Setting internal IPs for debug toolbar
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
    "127.0.0.1",
    "10.0.2.2",
]


# Django Querycount
# https://github.com/bradmontgomery/django-querycount
# Prints how many queries were executed, useful for the APIs.

MIDDLEWARE += ["querycount.middleware.QueryCountMiddleware"]


# nplusone
# For more information, see the project:
# https://github.com/jmcarp/nplusone

INSTALLED_APPS += ["nplusone.ext.django"]

MIDDLEWARE.insert(0, "nplusone.ext.django.NPlusOneMiddleware")

NPLUSONE_RAISE = True
NPLUSONE_WHITELIST = [
    {"model": "admin.*"},
]


# Disable persistent DB connections
# https://docs.djangoproject.com/en/4.2/ref/databases/#caveats

DATABASES["default"]["CONN_MAX_AGE"] = 0
