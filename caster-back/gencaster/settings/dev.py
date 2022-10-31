from .base import *  # noqa

DEBUG = True

CSRF_TRUSTED_ORIGINS = CSRF_TRUSTED_ORIGINS + [
    "http://localhost:*",
    "http://127.0.0.1:*",
]

CORS_ALLOW_ALL_ORIGINS = True
