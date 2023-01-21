"""
ASGI config for gencaster project.
"""
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path
from strawberry.channels import GraphQLWSConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gencaster.settings.dev")

if not os.environ.get("SUPERCOLLIDER_HOST") or os.environ.get("SUPERCOLLIDER_PORT"):
    print(
        "Environment variables SUPERCOLLIDER_HOST and SUPERCOLLIDER_PORT are unset - SC communication may not work"
    )

print(f"### STARTING SERVER WITH {os.environ['DJANGO_SETTINGS_MODULE']} ###")

django_asgi_app = get_asgi_application()


from .schema import schema

websocket_urlpatterns = [
    re_path(
        r"graphql",
        GraphQLWSConsumer.as_asgi(
            schema=schema,
        ),
    ),
]

application = ProtocolTypeRouter(
    {
        "http": URLRouter([re_path("^", django_asgi_app)]),  # type: ignore
        "websocket": URLRouter(websocket_urlpatterns),
    }
)
