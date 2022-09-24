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


def acknowledge_handler(client_address: Tuple[str, int], address: str, ack_uuid: str):
    try:
        instruction: StreamInstruction = StreamInstruction.objects.get(uuid=ack_uuid)
        instruction.acknowledged_time = timezone.now()
        instruction.save()
        log.info(f"Acknowledged instruction {instruction}")
    except StreamInstruction.DoesNotExist:
        log.error(f"Could not find stream instruction {ack_uuid}")


def live_handler(client_address: Tuple[str, int], address: str, *osc_args: List[Any]):
    # transforms [k1, v1, k2, v2, ...] to {k1: v1, k2:v2, ...}
    message: Dict[str, Any] = dict(zip(osc_args[0::2], osc_args[1::2]))  # type: ignore

    point: StreamPoint
    point, created = StreamPoint.objects.get_or_create(
        host=client_address[0],
        port=message["scLangPort"],
    )
    point.last_live = timezone.now()
    point.use_input = bool(message.get("useInput"))
    point.janus_in_port = message.get("janusInPort")
    point.janus_out_port = message.get("janusOutPort")
    point.janus_in_room = message.get("janusInRoom")
    point.janus_out_room = message.get("janusOutRoom")
    point.janus_public_ip = message.get("janusPublicIp")
    point.sc_name = message.get("scName")
    point.save()

    if created:
        log.info(f"Found new stream point: {point}")
    else:
        log.debug(f"Received live signal from {point}")


dispatcher = Dispatcher()
dispatcher.map("/acknowledge", acknowledge_handler, needs_reply_address=True)
dispatcher.map("/live", live_handler, needs_reply_address=True)

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
