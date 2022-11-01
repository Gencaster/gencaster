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
]

CORS_ALLOWED_ORIGINS = [
    "https://editor.dev.gencaster.org",
    "https://dev.gencaster.org",
    "https://backend.dev.gencaster.org",
]
