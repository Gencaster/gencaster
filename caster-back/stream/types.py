from datetime import timedelta
from typing import Optional
from uuid import UUID

import strawberry
import strawberry.django
from django.conf import settings
from django.utils import timezone
from strawberry import auto
from strawberry.file_uploads import Upload
from strawberry_django.filters import FilterLookup

from . import frontend_types, models


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
    num_listeners: auto
    stream_point: "StreamPoint"


@strawberry.django.filters.filter(models.AudioFile)
class AudioFileFilter:
    name: FilterLookup[str]
    auto_generated: bool
    description: FilterLookup[str]


@strawberry.django.type(models.AudioFile, filters=AudioFileFilter, pagination=True)
class AudioFile:
    uuid: auto
    file: auto
    name: auto
    description: auto
    auto_generated: auto
    created_date: auto


@strawberry.input
class AddAudioFile:
    file: Upload
    description: str
    file_name: str
    name: str


@strawberry.input
class UpdateAudioFile:
    description: Optional[str]
    name: Optional[str]


@strawberry.django.type(models.StreamInstruction)
class StreamInstruction:
    uuid: auto
    created_date: auto
    modified_date: auto
    instruction_text: auto
    state: auto
    return_value: auto
    frontend_display: frontend_types.Dialog


@strawberry.type
class StreamInfo:
    stream: Stream
    stream_instruction: Optional[StreamInstruction]


@strawberry.type
class NoStreamAvailable:
    """
    Matches :class:`gencaster.stream.exceptions.NoStreamAvailable`.
    """

    error: str = "No stream available"


@strawberry.type
class InvalidAudioFile:
    """
    Matches :class:`gencaster.stream.exceptions.InvalidAudioFile`.
    """

    error: str = "No valid audio file"


# combined types - can't be declared as type annotation

StreamInfoResponse = strawberry.union(
    "StreamInfoResponse", [StreamInfo, frontend_types.Dialog, NoStreamAvailable]
)

AudioFileUploadResponse = strawberry.union(
    "AudioFileUploadResponse", [AudioFile, InvalidAudioFile]
)


@strawberry.django.type(models.StreamVariable)
class StreamVariable:
    uuid: auto
    key: auto
    value: auto
    stream: Stream
    stream_to_sc: auto


@strawberry.input
class StreamVariableInput:
    stream_uuid: UUID
    key: str
    value: str
    stream_to_sc: bool = False


@strawberry.django.type(models.StreamLog)
class StreamLog:
    uuid: auto
    created_date: auto
    stream_point: StreamPoint
    stream: Stream
    origin: auto
    level: auto
    message: auto
    name: auto
