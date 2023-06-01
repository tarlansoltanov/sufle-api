"""
Django health check settings

For more information, see:
https://github.com/revsys/django-health-check
"""

from server.settings.components import config
from server.settings.components.common import INSTALLED_APPS

INSTALLED_APPS += [
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.contrib.migrations",
    "health_check.contrib.redis",
]

REDIS_URL = f"redis://:{config('REDIS_PASSWORD')}@{config('REDIS_HOST')}:{config('REDIS_PORT')}/0"  # noqa: E501
