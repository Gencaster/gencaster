from .base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ["*"]

TEST_RUNNER = "xmlrunner.extra.djangotestrunner.XMLTestRunner"
TEST_OUTPUT_FILE_NAME = "tests.xml"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",  # used for generating model image graphs
]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
