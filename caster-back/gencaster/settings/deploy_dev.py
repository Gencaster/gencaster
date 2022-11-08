from .base import *  # noqa

CSRF_TRUSTED_ORIGINS = [
    "https://dev.gencaster.org",
    "https://backend.dev.gencaster.org",
    "https://editor.dev.gencaster.org",
]

DEBUG = False

ALLOWED_HOSTS = [
    "*.gencaster.org",
    "gencaster.org",
    "dev.gencaster.org",
    "editor.dev.gencaster.org",
    "backend.dev.gencaster.org",
    "localhost",
    "127.0.0.1",
]

CORS_ALLOWED_ORIGINS = [
    "https://editor.dev.gencaster.org",
    "https://dev.gencaster.org",
    "https://backend.dev.gencaster.org",
]

SESSION_COOKIE_DOMAIN = ".dev.gencaster.org"
CSRF_COOKIE_DOMAIN = ".dev.gencaster.org"

CORS_ALLOW_CREDENTIALS = True

SESSION_COOKIE_SAMESITE = None

CSRF_COOKIE_SECURE = True
