import uuid
from typing import Any, Dict, List, Optional, Tuple

from django.test import TestCase
from pydantic import ValidationError

from osc_server.exceptions import MalformedOscMessage
from osc_server.models import OscTransformMixIn
from osc_server.server import OSCServer
from stream.models import StreamInstruction, StreamPoint
from stream.tests import StreamInstructionTestCase


class OSCTestTransform(OscTransformMixIn):
    pass


class OscServerTestCase(TestCase):
    @staticmethod
    def get_address() -> Tuple[str, int]:
        return ("172.0.0.2", 5012)

    def setUp(self) -> None:
        self.server = OSCServer()

    @staticmethod
    def get_message(d: Optional[Dict[str, Any]] = None) -> List[Any]:
        if d is None:
            d = {}
        message = ["hello", "world"]
        for k, v in d.items():
            message += [k, v]
        return message

    def test_parse_message(self):
        message = OscTransformMixIn._parse_message(*["hello", "world", "value", 2])
        self.assertDictEqual(
            message,
            {
                "hello": "world",
                "value": 2,
            },
        )

    def test_uneven_message(self):
        osc_message = self.get_message() + ["value"]
        with self.assertRaises(MalformedOscMessage):
            OscTransformMixIn._parse_message(osc_message)

    def test_unknown_uuid_message(self):
        osc_message = self.get_message(
            {
                "uuid": str(uuid.uuid4()),
                "status": "RECEIVED",
            }
        )
        self.server.acknowledge_handler(self.get_address(), "/ack", *osc_message)
        self.assertEqual(StreamInstruction.objects.all().count(), 0)

    def test_known_uuid_message(self):
        instruction = StreamInstructionTestCase.get_stream_instruction()
        osc_message = self.get_message(
            {
                "uuid": str(instruction.uuid),
                "status": "RECEIVED",
            }
        )
        self.server.acknowledge_handler(self.get_address(), "/ack", *osc_message)
        instruction.refresh_from_db()
        self.assertEqual(instruction.state, StreamInstruction.InstructionState.RECEIVED)

        osc_message = self.get_message(
            {
                "uuid": str(instruction.uuid),
                "status": "FINISHED",
            }
        )

        self.server.acknowledge_handler(self.get_address(), "/ack", *osc_message)
        instruction.refresh_from_db()
        self.assertEqual(instruction.state, StreamInstruction.InstructionState.FINISHED)

    def get_beacon_message(self) -> Dict[str, Any]:
        return {
            "synth_port": 5000,
            "lang_port": 5005,
            "janus_out_port": 1000,
            "janus_in_port": 1010,
            "janus_out_room": 1,
            "janus_in_room": 2,
            "janus_public_ip": "127.0.0.6",
            "use_input": 1,
            "osc_backend_host": "127.0.0.1",
            "osc_backend_port": 5039,
            "name": "Hello world",
        }

    def test_beacon(self):
        osc_message = self.get_message(self.get_beacon_message())

        self.server.beacon_handler(self.get_address(), "/beacon", *osc_message)

        self.assertEqual(StreamPoint.objects.all().count(), 1)
        stream_point: StreamPoint = StreamPoint.objects.first()  # type: ignore
        self.assertTrue(stream_point.is_online())

        # test update
        self.server.beacon_handler(self.get_address(), "/beacon", *osc_message)
        self.assertEqual(StreamPoint.objects.all().count(), 1)
        self.assertEqual(
            stream_point.sc_name,
            "Hello world",
        )

    def test_invalid_beacon(self):
        beacon_message = self.get_beacon_message()
        del beacon_message["lang_port"]
        with self.assertRaises(ValidationError):
            self.server.beacon_handler(
                self.get_address(), "/beacon", *self.get_message(beacon_message)
            )
