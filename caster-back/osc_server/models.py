"""
Models
======

Allows to use some static type checks for messages receiving from SuperCollider.

.. _OSC auth mixin:

.. pydantic:: osc_server.models.OSCAuthMixin

.. _OSC acknowledge message:

.. pydantic:: osc_server.models.SCAcknowledgeMessage

.. _OSC beacon message:

.. pydantic:: osc_server.models.SCBeaconMessage

.. _OSC remote action message:

.. pydantic:: osc_server.models.RemoteActionMessage

"""

import logging
import os
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, ValidationError, validator

from .exceptions import MalformedOscMessage, OscBackendAuthException

PASSWORD: str = os.environ.get("BACKEND_OSC_PASSWORD", "helloSC")
PROTOCOL_VERSION: str = "0.1"

log = logging.getLogger()


class OscTransformMixIn:
    """Transforms a flat OSC array

    .. code-block:: python

        [k1, v1, k2, v2]

    to a python dictionary

    .. code-block:: python

        {k1: v1, k2:v2}

    """

    @staticmethod
    def _parse_message(*osc_message: Any) -> Dict[str, Any]:
        if len(osc_message) % 2 != 0:
            raise MalformedOscMessage(
                f"OSC message is not sent as tuples: {osc_message}"
            )
        return dict(zip(osc_message[0::2], osc_message[1::2]))

    @classmethod
    def from_osc_args(cls, *osc_args):
        """Converts the OSC args into a dict."""
        message = cls._parse_message(*osc_args)
        try:
            c = cls(**message)  # type: ignore
        except ValidationError as e:
            log.error(f"Invalid message {message}")
            raise e
        return c


class GenCasterStatusEnum(str, Enum):
    """Status of our callback."""

    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    READY = "READY"
    FINISHED = "FINISHED"
    BEACON = "BEACON"
    RECEIVED = "RECEIVED"


class SCAcknowledgeMessage(OscTransformMixIn, BaseModel):
    """See :class:`~stream.models.StreamInstruction`."""

    uuid: str = Field(description="UUID from :class:`stream.models.StreamInstruction`")
    status: GenCasterStatusEnum
    return_value: Optional[str] = Field(
        description="Allows to store a return value in the database if given."
    )


class SCBeaconMessage(OscTransformMixIn, BaseModel):
    """Will create a :class:`~stream.models.StreamPoint`."""

    name: str
    synth_port: int
    lang_port: int
    janus_out_port: int
    janus_in_port: int
    janus_out_room: int
    janus_in_room: int
    janus_public_ip: str
    use_input: bool
    osc_backend_host: str
    osc_backend_port: int


class RemoteActionType(str, Enum):
    """Requests an action on SuperCollider instance."""

    code = "code"
    speak = "speak"


class OSCAuthMixin(BaseModel):
    """Allows to validate a given password for backends."""

    password: str

    @validator("password")
    def check_password(cls, v):
        if v != PASSWORD:
            raise OscBackendAuthException("Invalid password")
        return v


class RemoteActionMessage(OscTransformMixIn, OSCAuthMixin, BaseModel):
    """Sends message to SuperCollider cluster."""

    action: RemoteActionType
    cmd: str
    target: Optional[str]
    protocol_version: str = Field(
        description="Can be used to upgrade our communication by rejecting older clients/messages"
    )

    @validator("protocol_version")
    def validate_protocol_version(cls, v):
        if v != PROTOCOL_VERSION:
            raise MalformedOscMessage(
                f"Invalid protocol version {v} (expected {PROTOCOL_VERSION})"
            )
        return v
