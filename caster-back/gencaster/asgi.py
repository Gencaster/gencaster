"""
ASGI config for gencaster project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

import socketio
from pythonosc.udp_client import SimpleUDPClient
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gencaster.settings")

osc_client = SimpleUDPClient(
    address=os.environ["SUPERCOLLIDER_HOST"],
    port=int(os.environ["SUPERCOLLIDER_PORT"]),
)

osc_client.send_message("/foo", 400.0)

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
)

application = socketio.ASGIApp(
    sio,
    get_asgi_application(),
    socketio_path="socket.io",
)
