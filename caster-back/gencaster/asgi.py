"""
ASGI config for gencaster project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gencaster.settings.dev")

if not os.environ.get("SUPERCOLLIDER_HOST") or os.environ.get("SUPERCOLLIDER_PORT"):
    print(
        "Environment variables SUPERCOLLIDER_HOST and SUPERCOLLIDER_PORT are unset - SC communication may not work"
    )

print(f"### STARTING SERVER WITH {os.environ['DJANGO_SETTINGS_MODULE']} ###")

application = get_asgi_application()
