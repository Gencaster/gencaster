import uuid
from typing import Any, Dict, List, Optional, Tuple

from django.test import TestCase

from osc_server import (
    MalformedOscMessage,
    acknowledge_handler,
    beacon_handler,
    parse_message,
)
from stream.models import StreamInstruction, StreamPoint
from stream.tests import StreamInstructionTestCase


class OscServerTestCase(TestCase):
    @staticmethod
    def get_address() -> Tuple[str, int]:
        return ("172.0.0.2", 5012)

    @staticmethod
    def get_message(d: Optional[Dict[str, Any]] = None) -> List[Any]:
        if d is None:
            d = {}
        message = ["hello", "world"]
        for k, v in d.items():
            message += [k, v]
        return message

    def test_parse_message(self):
        osc_message = self.get_message({"value": 2})
        message = parse_message(osc_message)
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
            parse_message(osc_message)

    def test_unknown_uuid_message(self):
        osc_message = self.get_message({"uuid": str(uuid.uuid4())})
        acknowledge_handler(self.get_address(), "/ack", *osc_message)
        self.assertEqual(StreamInstruction.objects.all().count(), 0)

    def test_known_uuid_message(self):
        instruction = StreamInstructionTestCase.get_stream_instruction()
        osc_message = self.get_message(
            {
                "uuid": str(instruction.uuid),
                "status": "RECEIVED",
            }
        )
        acknowledge_handler(self.get_address(), "/ack", *osc_message)
        instruction.refresh_from_db()
        self.assertEqual(instruction.state, StreamInstruction.InstructionState.RECEIVED)

        osc_message = self.get_message(
            {
                "uuid": str(instruction.uuid),
                "status": "FINISHED",
            }
        )

        acknowledge_handler(self.get_address(), "/ack", *osc_message)
        instruction.refresh_from_db()
        self.assertEqual(instruction.state, StreamInstruction.InstructionState.FINISHED)

    def get_beacon_message(self) -> Dict[str, Any]:
        return {
            "useInput": 1,
            "janusInPort": 9003,
            "janusOutPort": 9004,
            "janusInRoom": 400,
            "janusOutRoom": 500,
            "janusPublicIP": "123.0.0.1",
            "name": "Hello world",
            "langPort": 12,
        }

    def test_beacon(self):
        osc_message = self.get_message(self.get_beacon_message())

        beacon_handler(self.get_address(), "/beacon", *osc_message)

        self.assertEqual(StreamPoint.objects.all().count(), 1)
        stream_point: StreamPoint = StreamPoint.objects.first()  # type: ignore
        self.assertTrue(stream_point.is_online())

        # test update
        beacon_handler(self.get_address(), "/beacon", *osc_message)
        self.assertEqual(StreamPoint.objects.all().count(), 1)
        self.assertEqual(
            stream_point.sc_name,
            "Hello world",
        )

    def test_invalid_beacon(self):
        beacon_message = self.get_beacon_message()
        del beacon_message["langPort"]
        with self.assertRaises(KeyError):
            beacon_handler(
                self.get_address(), "/beacon", *self.get_message(beacon_message)
            )
