"""
Deploy Dev
==========

Settings for deploying "*production*" dev environment on the server via Docker.
"""
import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

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

if public_ip := os.environ.get("BACKEND_PUBLIC_IP"):
    ALLOWED_HOSTS += [public_ip]

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
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )
