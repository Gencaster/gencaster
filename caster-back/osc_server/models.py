import logging
import os
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, ValidationError, validator

from .exceptions import MalformedOscMessage, OscBackendAuthException

PASSWORD: str = os.environ.get("BACKEND_OSC_PASSWORD", "helloSC")
PROTOCOL_VERSION: str = "0.1"

log = logging.getLogger()


class OscTransformMixIn:
    @staticmethod
    def _parse_message(*osc_message: Any) -> Dict[str, Any]:
        """transforms [k1, v1, k2, v2, ...] to {k1: v1, k2:v2, ...}"""
        if len(osc_message) % 2 != 0:
            raise MalformedOscMessage(
                f"OSC message is not sent as tuples: {osc_message}"
            )
        return dict(zip(osc_message[0::2], osc_message[1::2]))

    @classmethod
    def form_osc_args(cls, *osc_args):
        message = cls._parse_message(*osc_args)
        try:
            c = cls(**message)  # type: ignore
        except ValidationError as e:
            log.error(f"Invalid message {message}")
            raise e
        return c


class GenCasterStatusEnum(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    READY = "READY"
    FINISHED = "FINISHED"
    BEACON = "BEACON"
    RECEIVED = "RECEIVED"


class SCAcknowledgeMessage(OscTransformMixIn, BaseModel):
    uuid: str
    status: GenCasterStatusEnum
    return_value: Optional[str]


class SCBeaconMessage(OscTransformMixIn, BaseModel):
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
    code = "code"
    speak = "speak"


class OSCAuthMixin(BaseModel):
    password: str

    @validator("password")
    def check_password(cls, v):
        if v != PASSWORD:
            raise OscBackendAuthException("Invalid password")
        return v


class RemoteActionMessage(OscTransformMixIn, OSCAuthMixin, BaseModel):
    action: RemoteActionType
    cmd: str
    target: Optional[str]
    protocol_version: str

    @validator("protocol_version")
    def validate_protocol_version(cls, v):
        if v != PROTOCOL_VERSION:
            raise MalformedOscMessage(
                f"Invalid protocol version {v} (expected {PROTOCOL_VERSION})"
            )
        return v
