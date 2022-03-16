from tabnanny import verbose
import uuid
import logging

from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib import admin


log = logging.getLogger(__name__)


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
