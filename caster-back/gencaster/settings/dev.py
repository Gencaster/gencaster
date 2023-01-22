"""
Development
===========

Configures settings to allow access from local node environments.
"""

from .base import *  # noqa

DEBUG = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS

CORS_ALLOW_CREDENTIALS = True

SESSION_COOKIE_SECURE = False
SESSION_COOKIE_DOMAIN = None

# forces us to use 127.0.0.1 instead of localhost
# b/c otherwise the browser
# will not share our cookie with the editor/frontend
SESSION_COOKIE_DOMAIN = "127.0.0.1"
