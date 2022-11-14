import logging
import uuid
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Dict

from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from pythonosc.udp_client import SimpleUDPClient

from .exceptions import NoStreamAvailable

log = logging.getLogger(__name__)


@dataclass
class OSCMessage:
    address: str
    data: Any

    @classmethod
    def from_dict(cls, address: str, data: Dict):
        # todo: assert depth = 1
        # transform {k1: v1, k2: v2, ...} to [(k1, v1), (k2, v2), ...]
        tuples = [(k, v) for k, v in data.items()]
        # and now to [k1, v1, k2, v2, ...]
        data_list = [item for sublist in tuples for item in sublist]

        return cls(address=address, data=data_list)


class StreamPointManager(models.Manager):
    def free_stream_points(self) -> models.QuerySet["StreamPoint"]:
        last_online_time = timezone.now() - timedelta(seconds=60)
        return self.exclude(streams__active=True).filter(last_live__gt=last_online_time)


class StreamPoint(models.Model):
    objects = StreamPointManager()

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    host = models.CharField(max_length=255, verbose_name=_("SuperCollider host"))
    port = models.IntegerField(verbose_name=_("SuperCollider port"))

    use_input = models.BooleanField(
        default=False,
        verbose_name=_("Use input"),
        help_text=_("Accepts to send audio input"),
    )

    janus_in_port = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("Jauns in port"),
        help_text=_("RTP port where Janus streams the audio its received from user"),
    )

    janus_out_port = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("Janus out port"),
        help_text=_(
            "RTP port where SuperCollider/gstreamer streams its audio to Janus"
        ),
    )

    janus_in_room = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("Janus in room"),
        help_text=_(
            "Audiobridge room ID under which Janus can send audio to SuperCollider"
        ),
    )

    janus_out_room = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Jauns out room"),
        help_text=_(
            "Streaming room ID under which Janus serves audio from SuperCollider"
        ),
    )

    janus_public_ip = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_("Janus public IP"),
        help_text=_("IP or Hostname under which the janus instance is reachable"),
    )

    sc_name = models.CharField(
        max_length=128,
        null=True,
        verbose_name=_("SuperCollider name"),
        help_text=_(
            "Internal name of the SuperCollider instance on the host, necessary for gstreamer"
        ),
    )

    last_live = models.DateTimeField(
        verbose_name=_("Last live signal"),
        help_text=_("Last live signal from SuperCollider server"),
        null=True,
    )

    @admin.display(
        boolean=True,
        description=_("Live signal within last 60 sec"),
    )
    def is_online(self) -> bool:
        if not self.last_live:
            return False
        return (timezone.now() - self.last_live).seconds < 60

    def send_osc_message(self, osc_message: OSCMessage):
        SimpleUDPClient(self.host, self.port).send_message(
            address=osc_message.address, value=osc_message.data
        )

    class Meta:
        unique_together = ["host", "port"]
        ordering = ["-last_live", "host", "port"]
        verbose_name = _("Stream Endpoint")
        verbose_name_plural = _("Stream Endpoints")

    def __str__(self) -> str:
        return f"Stream Endpoint {self.host}:{self.port}"


class StreamManager(models.Manager):
    def get_free_stream(self) -> "Stream":
        free_stream_points = StreamPoint.objects.free_stream_points()
        if free_stream_points:
            return self.create(  # type: ignore
                stream_point=free_stream_points.first(),
            )
        else:
            raise NoStreamAvailable()

    def disconnect_all_streams(self):
        stream: Stream
        for stream in Stream.objects.filter(active=True):
            stream.disconnect()


class Stream(models.Model):
    objects = StreamManager()

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    stream_point = models.ForeignKey(
        "stream.StreamPoint",
        on_delete=models.CASCADE,
        related_name="streams",
        verbose_name=_("Associated instance"),
    )

    active = models.BooleanField(
        verbose_name=_("Is stream currently in use"),
        default=True,
    )

    def disconnect(self):
        log.info(f"Disconnect stream {self.uuid}")
        self.active = False
        self.save()

    class Meta:
        ordering = ["-created_date", "stream_point"]
        verbose_name = _("Stream")
        verbose_name_plural = _("Streams")

    def __str__(self) -> str:
        return f"Stream on {self.stream_point}"


class StreamInstruction(models.Model):
    class InstructionState(models.TextChoices):
        SUCCESS = "SUCCESS", _("SUCCESS")
        FAILURE = "FAILURE", _("FAILURE")
        READY = "READY", _("READY")
        UNACKNOWLEDGED = "UNACKNOWLEDGED", _("UNACKNOWLEDGED")
        FINISHED = "FINISHED", _("FINISHED")
        RECEIVED = "RECEIVED", _("RECEIVED")

        def from_sc_string(self, sc_string: str):
            """Converts a string from SuperCollider to our typed state choices.

            .. todo::

                return type
            """
            try:
                return getattr(self, sc_string.upper())
            except AttributeError:
                log.error(f'Could not parse "{sc_string}" state to django state')
                return self.FAILURE

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    stream = models.ForeignKey(
        "stream.Stream",
        on_delete=models.CASCADE,
        related_name="instructions",
    )

    instruction_text = models.TextField(
        verbose_name=_("Instruction that gets transmitted via OSC"),
    )

    state = models.TextField(
        verbose_name="Instruction state",
        max_length=100,
        choices=InstructionState.choices,
        default=InstructionState.UNACKNOWLEDGED,
    )

    class Meta:
        ordering = ["-created_date", "stream"]
        verbose_name = _("Stream Instruction")
        verbose_name_plural = _("Stream Instructions")

    def __str__(self) -> str:
        return f"{self.uuid} ({self.state})"
