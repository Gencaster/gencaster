from .base import *  # noqa

CSRF_TRUSTED_ORIGINS = ["https://dev.gencaster.org"]

DEBUG = False

ALLOWED_HOSTS = [
    "*.gencaster.org",
    "gencaster.org",
]

CORS_ALLOWED_ORIGINS = [
    "https://editor.dev.gencaster.org",
]
