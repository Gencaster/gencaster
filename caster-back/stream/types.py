from datetime import timedelta
from typing import Optional

import strawberry
import strawberry.django
from django.conf import settings
from django.utils import timezone
from strawberry import auto
from strawberry.file_uploads import Upload

from . import models


@strawberry.django.filters.filter(models.StreamPoint, lookups=True)
class StreamPointFilter:
    uuid: auto
    janus_in_port: auto


@strawberry.django.type(models.StreamPoint, filters=StreamPointFilter)
class StreamPoint:
    uuid: auto
    created_date: auto
    modified_date: auto
    host: auto
    port: auto
    use_input: auto
    janus_in_port: auto
    janus_out_port: auto
    last_live: auto
    janus_in_room: auto
    janus_out_room: auto

    @classmethod
    def get_queryset(cls, queryset, info):
        # .exclude(streams__active=True)
        return queryset.filter(
            last_live__gt=timezone.now()
            - timedelta(seconds=settings.STREAM_MAX_BEACON_SEC)
        )


@strawberry.django.type(models.Stream)
class Stream:
    uuid: auto
    created_date: auto
    modified_date: auto
    active: auto
    stream_point: "StreamPoint"


@strawberry.django.type(models.AudioFile)
class AudioFile:
    uuid: auto
    file: auto
    description: auto


@strawberry.input
class AddAudioFile:
    file: Upload
    description: str
    file_name: str


@strawberry.django.type(models.StreamInstruction)
class StreamInstruction:
    uuid: auto
    created_date: auto
    modified_date: auto
    instruction_text: auto
    state: auto
    return_value: auto


@strawberry.type
class StreamInfo:
    stream: Stream
    stream_instruction: Optional[StreamInstruction]
