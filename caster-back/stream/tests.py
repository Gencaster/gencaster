import io
import logging
from datetime import timedelta
from typing import List
from unittest import mock

from django.test import TestCase
from django.utils import timezone
from mixer.backend.django import mixer

from .exceptions import NoStreamAvailableException
from .models import AudioFile, Stream, StreamInstruction, StreamPoint, TextToSpeech

logging.disable(logging.CRITICAL)


class StreamPointTestCase(TestCase):
    def setUp(self):
        pass

    @staticmethod
    def get_stream_point(last_live_sec=1) -> StreamPoint:
        return mixer.blend(  # type: ignore
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
            StreamPoint.objects.free_stream_points().first().uuid, stream_point.uuid  # type: ignore
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
        return mixer.blend(  # type: ignore
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
        with self.assertRaises(NoStreamAvailableException):
            Stream.objects.get_free_stream()

    def test_stream_not_online(self):
        stream_point = StreamPointTestCase.get_stream_point(last_live_sec=5000)
        with self.assertRaises(NoStreamAvailableException):
            Stream.objects.get_free_stream()

    def test_all_streampoints_taken(self):
        for _ in range(2):
            stream_point = StreamPointTestCase.get_stream_point()
            stream = self.get_stream(active=True, stream_point=stream_point)
        with self.assertRaises(NoStreamAvailableException):
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


class AudioFileTestCase(TestCase):
    @staticmethod
    def get_audio_file(**kwargs) -> AudioFile:
        return mixer.blend(  # type: ignore
            AudioFile,
            **kwargs,
        )  # type: ignore

    def test_creation(self):
        file_content = io.BytesIO(b"hello_world")
        audio_file = AudioFile.from_file(file_content)
        self.assertEqual(AudioFile.objects.all().count(), 1)
        self.assertEqual(audio_file.file.read(), b"hello_world")

    def test_str(self):
        audio_file = self.get_audio_file()
        self.assertTrue(str(audio_file.file) in str(audio_file))


class TextToSpeechTestCase(TestCase):
    @staticmethod
    def get_text_to_speech(**kwargs) -> TextToSpeech:
        return mixer.blend(TextToSpeech, **kwargs)  # type: ignore

    def test_existing_one(self):
        existing = self.get_text_to_speech(text="hello world")
        new = TextToSpeech.create_from_text(ssml_text="hello world")
        self.assertEqual(existing, new)

    @mock.patch("stream.models.texttospeech")
    def test_mock_call(self, tts):
        tts.TextToSpeechClient.return_value.synthesize_speech.return_value.audio_content = (
            b"hello_world"
        )
        t = TextToSpeech.create_from_text("foo")
        self.assertEqual(t.audio_file.file.read(), b"hello_world")
        self.assertEqual(TextToSpeech.objects.all().count(), 1)

    def test_str(self):
        t = self.get_text_to_speech(text="Hello world")
        self.assertTrue("Hello world" in str(t))
