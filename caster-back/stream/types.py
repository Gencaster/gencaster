import strawberry
import strawberry.django
from strawberry import auto

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


@strawberry.django.type(models.Stream)
class Stream:
    uuid: auto
    created_date: auto
    modified_date: auto
    active: auto
    stream_point: "StreamPoint"
