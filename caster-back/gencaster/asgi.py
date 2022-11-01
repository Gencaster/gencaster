"""
ASGI config for gencaster project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from pythonosc.udp_client import SimpleUDPClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gencaster.settings.dev")

if not os.environ.get("SUPERCOLLIDER_HOST") or os.environ.get("SUPERCOLLIDER_PORT"):
    print(
        "Environment variables SUPERCOLLIDER_HOST and SUPERCOLLIDER_PORT are unset - SC communication may not work"
    )

osc_client = SimpleUDPClient(
    address=os.environ.get("SUPERCOLLIDER_HOST", "localhost"),
    port=int(os.environ.get("SUPERCOLLIDER_PORT", 57120)),
)

# osc_client.send_message("/foo", 400.0)

print(f"### STARTING SERVER WITH {os.environ['DJANGO_SETTINGS_MODULE']} ###")

application = get_asgi_application()
