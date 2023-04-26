"""
Server
======

A naive server to receive OSC messages from SuperCollider.
"""

import logging
import os
from typing import Any, Callable, Dict, List, Optional, Tuple

import django

django.setup()  # type: ignore

from django.utils import timezone
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

from story_graph.markdown_parser import md_to_ssml
from stream.models import StreamInstruction, StreamPoint, TextToSpeech

from .models import (
    RemoteActionMessage,
    RemoteActionType,
    SCAcknowledgeMessage,
    SCBeaconMessage,
)

log = logging.getLogger(__name__)


class OSCServer:
    """
    Uses pythonosc to map the routes

    .. list-table:: Routes
        :header-rows: 1

        * - route
          - method
          - message

        * - `/beacon`
          - :func:`~OSCServer.beacon_handler`
          - :ref:`OSC beacon message`

        * - `/acknowledge_handler`
          - :func:`~OSCServer.acknowledge_handler`
          - :ref:`OSC acknowledge message`

        * - `/remote/action`
          - :func:`~OSCServer.remote_action_handler`
          - :ref:`OSC remote action message`

    """

    def __init__(self):
        self._dispatcher: Optional[Dispatcher] = None
        self.mapper: Dict[str, Callable[[Tuple[str, int], str, List[Any]], None]] = {
            "/beacon": self.beacon_handler,
            "/acknowledge": self.acknowledge_handler,
            "/remote/action": self.remote_action_handler,
        }

    def serve_blocking(self, host: str = "0.0.0.0", port: int = 7000):
        dispatcher = self.get_dispatcher()

        server = BlockingOSCUDPServer((host, port), dispatcher)
        try:
            log.info(
                f"Start blocking OSC server on port {port} with routes: {', '.join([k for k in dispatcher._map.keys()])}"
            )
            server.serve_forever()
        except KeyboardInterrupt:
            log.info("Received stop signal")
            server.shutdown()
        finally:
            log.info("Close server")
            server.server_close()

    def beacon_handler(
        self, client_address: Tuple[str, int], address: str, *osc_args: List[Any]
    ) -> None:
        """Accepts a beacon from SuperCollider and creates a
        :class:`~StreamPoint` from it so it gets discovered by the backend.
        """
        beacon_message = SCBeaconMessage.from_osc_args(*osc_args)

        point: StreamPoint
        point, created = StreamPoint.objects.get_or_create(
            host=client_address[0],
            port=beacon_message.lang_port,
        )

        point.last_live = timezone.now()
        point.use_input = beacon_message.use_input
        point.janus_in_port = beacon_message.janus_in_port
        point.janus_out_port = beacon_message.janus_out_port
        point.janus_in_room = beacon_message.janus_in_room
        point.janus_out_room = beacon_message.janus_out_room
        point.janus_public_ip = beacon_message.janus_public_ip
        point.sc_name = beacon_message.name
        point.save()

        if created:
            log.info(f"Found new stream point: {point}")
        else:
            log.debug(f"Received live signal from {point}")

    def acknowledge_handler(
        self, client_address: Tuple[str, int], address: str, *osc_args: List[Any]
    ) -> None:
        """Acknowledges a message and updates its associated
        :class:`~story_graph.models.StreamInstruction`.
        """
        ack_message = SCAcknowledgeMessage.from_osc_args(*osc_args)

        try:
            stream_instruction: StreamInstruction = StreamInstruction.objects.get(
                uuid=ack_message.uuid,
            )
        except StreamInstruction.DoesNotExist:
            log.error(f"Could not find StreamInstruction with UUID {ack_message.uuid}")
            return

        stream_instruction.state = StreamInstruction.InstructionState.from_sc_string(
            ack_message.status
        )
        if ack_message.return_value:
            stream_instruction.return_value = ack_message.return_value
        stream_instruction.save()

    def remote_action_handler(
        self, client_address: Tuple[str, int], address: str, *osc_args: List[Any]
    ) -> None:
        """Remote actions are used to trigger actions on a SuperCollider instance
        and can be send in form of a :class:`~stream.models.StreamInstruction`
        or raw from a local running SuperCollider instance which
        can be used to live code the SuperCollider instances managed by Gencaster.
        """
        remote_message = RemoteActionMessage.from_osc_args(*osc_args)

        stream_points = StreamPoint.objects.free_stream_points().filter()
        if remote_message.target:
            stream_points = stream_points.filter(janus_out_room=remote_message.target)

        if stream_points.count() == 0:
            log.error(
                f"Could not find active matching streaming point with filter {remote_message.target}"
            )
            return

        if remote_message.action == RemoteActionType.code:
            log.info(f"Execute on {remote_message.target}: '{remote_message.cmd}'")
            for stream_point in stream_points.all():
                stream_point.send_raw_instruction(remote_message.cmd)
        elif remote_message.action == RemoteActionType.speak:
            log.info(f"Speak on {remote_message.target}: '{remote_message.cmd}'")

            # to allow for caching when sending to multiple stream_points
            # we create the text here so the streaming points can rely on the cache
            ssml_text = md_to_ssml(remote_message.cmd)
            TextToSpeech.create_from_text(ssml_text)

            for stream_point in stream_points.all():
                stream_point.speak_on_stream(ssml_text)
        else:
            log.critical(f"Unknown action {remote_message.action}")

    def get_dispatcher(self) -> Dispatcher:
        if self._dispatcher is not None:
            return self._dispatcher

        self._dispatcher = Dispatcher()
        for address, callback in self.mapper.items():
            self._dispatcher.map(address, callback, needs_reply_address=True)  # type: ignore
        return self._dispatcher


if __name__ == "__main__":  # pragma: no cover
    port = int(os.environ.get("BACKEND_OSC_PORT", 7000))

    logging_level = os.environ.get("BACKEND_OSC_LOG_LEVEL", "INFO")

    server = OSCServer()
    server.serve_blocking(port=port)
