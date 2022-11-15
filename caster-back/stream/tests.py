import logging
from datetime import timedelta
from typing import List
from unittest import mock

from django.test import TestCase
from django.utils import timezone
from mixer.backend.django import mixer

from .exceptions import NoStreamAvailable
from .models import Stream, StreamInstruction, StreamPoint

logging.disable(logging.CRITICAL)


class StreamPointTestCase(TestCase):
    def setUp(self):
        pass

    @staticmethod
    def get_stream_point(last_live_sec=1) -> StreamPoint:
        return mixer.blend(
            StreamPoint, last_live=timezone.now() - timedelta(seconds=last_live_sec)
        )  # type: ignore

    def test_no_free_stream(self):
        stream_points: List[StreamPoint] = mixer.cycle(5).blend(
            StreamPoint, last_live=timezone.now() - timedelta(seconds=120)
        )
        self.assertIsNone(StreamPoint.objects.free_stream_points().first())

    def test_free_stream_point(self):
        stream_point: StreamPoint = mixer.blend(
            StreamPoint, last_live=timezone.now() - timedelta(seconds=5)
        )  # type: ignore
        # add some non-live examples
        mixer.cycle(5).blend(
            StreamPoint, last_live=timezone.now() - timedelta(seconds=120)
        )
        self.assertEqual(
            StreamPoint.objects.free_stream_points().first().uuid, stream_point.uuid
        )
        self.assertTrue(stream_point.is_online())

    def test_send_instruction(self):
        stream_point = self.get_stream_point()
        instruction: StreamInstruction = mixer.blend(
            StreamInstruction,
            stream_point=stream_point,
        )  # type: ignore

        self.assertEqual(
            instruction.state, StreamInstruction.InstructionState.UNACKNOWLEDGED
        )

        # @todo somehow check if client was actually called properly? :/
        with mock.patch(
            "stream.models.StreamPoint.client", new_callable=mock.PropertyMock()
        ) as m:
            stream_point.send_stream_instruction(instruction)

        self.assertEqual(instruction.state, StreamInstruction.InstructionState.SENT)

    def test_raw_instruction(self):
        stream_point = self.get_stream_point()

        instruction = '{"Hello World".postln;}'

        with mock.patch(
            "stream.models.StreamPoint.client", new_callable=mock.PropertyMock()
        ) as m:
            stream_point.send_raw_instruction(instruction)

        self.assertEqual(
            StreamInstruction.objects.filter(
                stream_point=stream_point,
                instruction_text=instruction,
                state=StreamInstruction.InstructionState.SENT,
            ).count(),
            1,
        )

    def test_offline(self):
        stream_point = self.get_stream_point(last_live_sec=5000)
        self.assertFalse(stream_point.is_online())

    def test_str(self):
        stream_point = self.get_stream_point()
        self.assertTrue(str(stream_point.host) in str(stream_point))


class StreamTestCase(TestCase):
    def get_stream(self, **kwargs) -> Stream:
        return mixer.blend(
            Stream,
            **kwargs,
        )  # type: ignore

    def test_get_free_stream(self):
        stream_point = StreamPointTestCase.get_stream_point()
        stream = Stream.objects.get_free_stream()
        self.assertEqual(
            stream.stream_point,
            stream_point,
        )

    def test_no_free_stream(self):
        with self.assertRaises(NoStreamAvailable):
            Stream.objects.get_free_stream()

    def test_stream_not_online(self):
        stream_point = StreamPointTestCase.get_stream_point(last_live_sec=5000)
        with self.assertRaises(NoStreamAvailable):
            Stream.objects.get_free_stream()

    def test_all_streampoints_taken(self):
        for _ in range(2):
            stream_point = StreamPointTestCase.get_stream_point()
            stream = self.get_stream(active=True, stream_point=stream_point)
        with self.assertRaises(NoStreamAvailable):
            Stream.objects.get_free_stream()

    def test_make_all_offline(self):
        for _ in range(2):
            stream = self.get_stream(active=True)
        stream = self.get_stream(active=True)

        stream.disconnect()
        self.assertFalse(stream.active)

        Stream.objects.disconnect_all_streams()

        self.assertEqual(
            Stream.objects.filter(active=True).count(),
            0,
        )

    def test_str(self):
        stream = self.get_stream()
        self.assertTrue(str(stream.stream_point) in str(stream))


class StreamInstructionTestCase(TestCase):
    @staticmethod
    def get_stream_instruction(**kwargs) -> StreamInstruction:
        return mixer.blend(StreamInstruction, **kwargs)  # type: ignore

    def test_instruction_state(self):
        self.assertEqual(
            StreamInstruction.InstructionState.from_sc_string("foobar"),
            StreamInstruction.InstructionState.FAILURE,
        )

        self.assertEqual(
            StreamInstruction.InstructionState.from_sc_string("SUCCESS"),
            StreamInstruction.InstructionState.SUCCESS,
        )

    def test_str(self):
        stream_instruction = self.get_stream_instruction()
        self.assertTrue(str(stream_instruction.uuid) in str(stream_instruction))
