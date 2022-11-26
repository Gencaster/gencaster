import logging
import os
from typing import Any, Callable, Dict, List, Tuple

import django

django.setup()  # type: ignore

from enum import Enum

from django.utils import timezone
from pydantic import BaseModel, validator
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

from story_graph.markdown_parser import md_to_ssml
from stream.models import StreamInstruction, StreamPoint

log = logging.getLogger(__name__)

STREAM_POINTS: Dict[str, StreamPoint] = {}
PASSWORD: str = os.environ.get("BACKEND_OSC_PASSWORD", "helloSC")


class GenCasterAuthException(Exception):
    pass


class GenCasterActionEnum(str, Enum):
    code = "code"
    speak = "speak"


class GenCasterOSCAuthMessage(BaseModel):
    password: str
    action: GenCasterActionEnum
    text: str
    target: str

    @validator("password")
    def check_password(cls, v):
        if v != PASSWORD:
            raise GenCasterAuthException("Invalid password")
        return v

    @staticmethod
    def _parse_message(osc_message: Any) -> Dict[str, Any]:
        """transforms [k1, v1, k2, v2, ...] to {k1: v1, k2:v2, ...}"""
        if len(osc_message) % 2 != 0:
            raise MalformedOscMessage(
                f"OSC message is not sent as tuples: {osc_message}"
            )
        return dict(zip(osc_message[0::2], osc_message[1::2]))

    @classmethod
    def form_osc_args(cls, *osc_args):
        message = cls._parse_message(osc_args)
        return cls(**message)


class OSCServer:
    def __init__(self):
        self._dispatcher: Dispatcher
        self.mapper: Dict[str, Callable[[Tuple[str, int], str, List[Any]], None]] = {
            "/beacon": self.beacon_handler,
        }

    def serve(self, host: str = "0.0.0.0", port: int = 8000):
        pass

    def beacon_handler(
        self, client_address: Tuple[str, int], address: str, *osc_args: List[Any]
    ) -> None:
        pass

    @property
    def dispatcher(self):
        if self._dispatcher is not None:
            return self._dispatcher

        self._dispatcher = Dispatcher()
        for address, callback in self.mapper.items():
            self._dispatcher.map(address, callback, needs_reply_address=True)  # type: ignore


class MalformedOscMessage(Exception):
    pass


def parse_message(osc_message: Any) -> Dict[str, Any]:
    """transforms [k1, v1, k2, v2, ...] to {k1: v1, k2:v2, ...}"""
    if len(osc_message) % 2 != 0:
        raise MalformedOscMessage(f"OSC message is not sent as tuples: {osc_message}")
    return dict(zip(osc_message[0::2], osc_message[1::2]))


def is_authorized(osc_message: Dict[str, Any]) -> bool:
    # idea: use two keys - first one is a hashed password, second is a random salt
    # and we need it to hash with the message to verify that it does not get
    # copy/pasted with a timecode?
    return bool(osc_message.get("password", None) == PASSWORD)


def acknowledge_handler(
    client_address: Tuple[str, int], address: str, *osc_args: List[Any]
) -> None:
    message = parse_message(osc_args)

    try:
        stream_instruction: StreamInstruction = StreamInstruction.objects.get(
            uuid=message["uuid"],
        )
    except StreamInstruction.DoesNotExist:
        log.error(
            f"Could not find StreamInstruction with UUID {message.get('uuid', 'unknown')}"
        )
        return

    stream_instruction.state = StreamInstruction.InstructionState.from_sc_string(message.get("status", "FAILURE"))  # type: ignore
    stream_instruction.return_value = message.get("returnValue", "")
    stream_instruction.save()


def beacon_handler(
    client_address: Tuple[str, int], address: str, *osc_args: List[Any]
) -> None:
    message = parse_message(osc_args)

    point: StreamPoint
    point, created = StreamPoint.objects.get_or_create(
        host=client_address[0],
        port=message["langPort"],
    )
    point.last_live = timezone.now()
    point.use_input = bool(message.get("useInput"))
    point.janus_in_port = message.get("janusInPort")
    point.janus_out_port = message.get("janusOutPort")
    point.janus_in_room = message.get("janusInRoom")
    point.janus_out_room = message.get("janusOutRoom")
    point.janus_public_ip = message.get("janusPublicIP")
    point.sc_name = message.get("name")
    point.save()

    if created:
        log.info(f"Found new stream point: {point}")
    else:
        log.debug(f"Received live signal from {point}")


def remote_action_handler(
    client_address: Tuple[str, int], address: str, *osc_args: List[Any]
) -> None:
    osc_message = GenCasterOSCAuthMessage.form_osc_args(*osc_args)

    stream_points = StreamPoint.objects.free_stream_points().filter()
    if osc_message.target.upper() != "BROADCAST":
        stream_points = stream_points.filter(janus_out_room=osc_message.target)

    if stream_points.count() == 0:
        log.error(f"Could not find matching streaming point {osc_message.target}")
        return

    if osc_message.action == GenCasterActionEnum.code:
        log.info(f"Execute on {osc_message.target}: '{osc_message.text}'")
        for stream_point in stream_points.all():
            stream_point.send_raw_instruction(osc_message.text)
    elif osc_message.action == GenCasterActionEnum.speak:
        log.info(f"Speak on {osc_message.target}: '{osc_message.text}'")
        for stream_point in stream_points.all():
            stream_point.speak_on_stream(md_to_ssml(osc_message.text))


dispatcher = Dispatcher()
dispatcher.map("/ack", acknowledge_handler, needs_reply_address=True)  # type: ignore
dispatcher.map("/beacon", beacon_handler, needs_reply_address=True)  # type: ignore

dispatcher.map("/remote/action", remote_action_handler, needs_reply_address=True)  # type: ignore

if __name__ == "__main__":  # pragma: no cover
    port = int(os.environ["BACKEND_OSC_PORT"])
    server = BlockingOSCUDPServer(("0.0.0.0", port), dispatcher)
    try:
        log.info(
            f"Start OSC server on {port} with routes: {', '.join([k for k in dispatcher._map.keys()])}"
        )
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("Received stop signal")
        server.shutdown()
    finally:
        log.info("Close server")
        server.server_close()
