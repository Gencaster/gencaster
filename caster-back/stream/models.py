from dataclasses import dataclass
import uuid
import logging

from pythonosc.udp_client import SimpleUDPClient
from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib import admin


log = logging.getLogger(__name__)


@dataclass
class OSCMessage:
    address: str
    data: any


class StreamPoint(models.Model):
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
        default=False, verbose_name=_("Accepts to send audio input")
    )

    janus_in_port = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("RTP port where Janus streams the audio its received from user"),
    )

    janus_out_port = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_(
            "RTP port where SuperCollider/gstreamer streams its audio to Janus"
        ),
    )

    janus_in_room = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_(
            "Audiobridge room ID under which Janus can send audio to SuperCollider"
        ),
    )

    janus_out_room = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_(
            "Streaming room ID under which Janus serves audio from SuperCollider"
        ),
    )

    janus_public_ip = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_("IP or Hostname under which the janus instance is reachable"),
    )

    sc_name = models.CharField(
        max_length=128,
        null=True,
        verbose_name=_(
            "Internal name of the SuperCollider instance on the host, necessary for gstreamer"
        ),
    )

    last_live = models.DateTimeField(
        verbose_name=_("Last live signal from SuperCollider server"),
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


class Stream(models.Model):
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

    acknowledged_time = models.DateTimeField()

    class Meta:
        ordering = ["-created_date", "stream"]
        verbose_name = _("Stream Instruction")
        verbose_name_plural = _("Stream Instructions")

    def __str__(self) -> str:
        return f"Stream Instruction {self.instruction_text[0:100]} for {self.stream}"
