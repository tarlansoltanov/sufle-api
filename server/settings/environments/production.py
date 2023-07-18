"""
Production Environment Settings for Django Project

These settings are specific to the production environment.
"""

from server.settings.components import config


# Production flags:
# https://docs.djangoproject.com/en/4.2/howto/deployment/

SECRET_KEY = config("DJANGO_SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [
    config("DOMAIN_NAME"),
    config("DOMAIN_IP"),
    # For nginx proxy:
    "web",
    # We need this value for `healthcheck` to work:
    "localhost",
]


# Staticfiles
# https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/

# This is a hack to allow a special flag to be used with `--dry-run`
# to test things locally.
_COLLECTSTATIC_DRYRUN = config(
    "DJANGO_COLLECTSTATIC_DRYRUN",
    cast=bool,
    default=False,
)

# Adding STATIC_ROOT to collect static files via 'collectstatic':
STATIC_ROOT = ".static" if _COLLECTSTATIC_DRYRUN else "/var/www/static"


# Media files
# https://docs.djangoproject.com/en/4.2/topics/files/

MEDIA_ROOT = "/var/www/media"

if not config("STAGING", cast=bool, default=False):
    # Security
    # https://docs.djangoproject.com/en/4.2/topics/security/

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SECURE_REDIRECT_EXEMPT = [
        # This is required for healthcheck to work:
        "^health/",
    ]

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    CSRF_TRUSTED_ORIGINS = [
        f'https://{config("DOMAIN_NAME")}',
    ]
