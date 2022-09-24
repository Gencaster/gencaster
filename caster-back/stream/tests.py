from datetime import timedelta
from typing import List

from django.test import TestCase
from django.utils import timezone
from mixer.backend.django import mixer

from .models import StreamPoint


class StreamPointTestCase(TestCase):
    def setUp(self):
        pass

    def test_no_free_stream(self):
        stream_points: List[StreamPoint] = mixer.cycle(5).blend(
            StreamPoint, last_live=timezone.now() - timedelta(seconds=120)
        )
        self.assertIsNone(StreamPoint.objects.free_stream_points().first())

    def test_free_stream_point(self):
        stream_point: StreamPoint = mixer.blend(
            StreamPoint, last_live=timezone.now() - timedelta(seconds=5)
        )
        # add some non-live examples
        mixer.cycle(5).blend(
            StreamPoint, last_live=timezone.now() - timedelta(seconds=120)
        )
        self.assertEqual(
            StreamPoint.objects.free_stream_points().first().uuid, stream_point.uuid
        )
