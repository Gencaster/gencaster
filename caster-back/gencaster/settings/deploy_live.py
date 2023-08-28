"""
Deploy Live
===========

Settings for deploying "*production*" environment on the server via Docker.
"""

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa

CSRF_TRUSTED_ORIGINS = [
    "https://live.gencaster.org",
    "https://backend.live.gencaster.org",
    "https://editor.live.gencaster.org",
]

DEBUG = False

ALLOWED_HOSTS = [
    "*.gencaster.org",
    "gencaster.org",
    "live.gencaster.org",
    "editor.live.gencaster.org",
    "backend.live.gencaster.org",
    "localhost",
    "127.0.0.1",
]

CORS_ALLOWED_ORIGINS = [
    "https://editor.live.gencaster.org",
    "https://live.gencaster.org",
    "https://backend.live.gencaster.org",
]

SESSION_COOKIE_DOMAIN = ".live.gencaster.org"
CSRF_COOKIE_DOMAIN = ".live.gencaster.org"

CORS_ALLOW_CREDENTIALS = True

SESSION_COOKIE_SAMESITE = None

CSRF_COOKIE_SECURE = True


if SENTRY_DSN := os.environ.get("SENTRY_DSN_CASTER_BACK", None):
    print("### SENTRY LOGGING ACTIVE ###")
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
        ],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.2,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )
