"""
Local development
=================

Switch to local sqlite database.
"""

from .dev import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}
