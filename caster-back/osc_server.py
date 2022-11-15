import logging
import os
from typing import Any, Dict, List, Tuple

import django
from django.utils import timezone
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

django.setup()

from stream.models import StreamInstruction, StreamPoint

log = logging.getLogger(__name__)


class MalformedOscMessage(Exception):
    pass


def parse_message(osc_message: Any) -> Dict[str, Any]:
    """transforms [k1, v1, k2, v2, ...] to {k1: v1, k2:v2, ...}"""
    if len(osc_message) % 2 != 0:
        raise MalformedOscMessage(f"OSC message is not sent as tuples: {osc_message}")
    return dict(zip(osc_message[0::2], osc_message[1::2]))


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


dispatcher = Dispatcher()
dispatcher.map("/ack", acknowledge_handler, needs_reply_address=True)  # type: ignore
dispatcher.map("/beacon", beacon_handler, needs_reply_address=True)  # type: ignore

if __name__ == "__main__":
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
