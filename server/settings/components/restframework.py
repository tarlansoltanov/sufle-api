"""
Django REST framework settings

For more information, see the documentation:
https://www.django-rest-framework.org/
"""

from server.settings.components.common import INSTALLED_APPS

INSTALLED_APPS += [
    "rest_framework",
]