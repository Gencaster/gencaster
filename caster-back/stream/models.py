import io
import logging
import uuid
from datetime import timedelta

from asgiref.sync import async_to_sync
from django.conf import settings
from django.contrib import admin
from django.core.files import File
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from google.cloud import texttospeech
from pythonosc.udp_client import SimpleUDPClient

from .exceptions import NoStreamAvailable

log = logging.getLogger(__name__)


class StreamPointManager(models.Manager["StreamPoint"]):
    def free_stream_points(self) -> models.QuerySet["StreamPoint"]:
        return async_to_sync(self.afree_stream_points)()  # type: ignore

    async def afree_stream_points(self) -> models.QuerySet["StreamPoint"]:
        return self.exclude(streams__active=True).filter(
            last_live__gt=timezone.now()
            - timedelta(seconds=settings.STREAM_MAX_BEACON_SEC)
        )


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

    @property
    def client(self) -> SimpleUDPClient:
        return SimpleUDPClient(address=self.host, port=self.port)

    def speak_on_stream(self, ssml_text: str):
        """Speaks on the stream

        :param ssml_text: See https://cloud.google.com/text-to-speech/docs/ssml
        """
        tts = TextToSpeech.create_from_text(ssml_text)
        self.play_audio_file(tts.audio_file)

    def play_audio_file(self, audio_file: "AudioFile"):
        sc_audio_file_path = f"/data/{audio_file.file.name}"
        sc_code = (
            f'{{Buffer.read(s, path: "{sc_audio_file_path}", action: {{|b| b.play;}})}}'
        )
        self.send_raw_instruction(sc_code)

    # todo make this async?
    def send_raw_instruction(self, instruction_text: str) -> "StreamInstruction":
        instruction: StreamInstruction = StreamInstruction.objects.create(
            stream_point=self,
            instruction_text=instruction_text,
        )
        self.send_stream_instruction(instruction)
        return instruction

    def send_stream_instruction(self, instruction: "StreamInstruction") -> None:
        self.client.send_message(
            address="/instruction",
            value=[str(instruction.uuid), instruction.instruction_text],
        )
        instruction.state = StreamInstruction.InstructionState.SENT
        instruction.save()

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


class StreamManager(models.Manager):
    def get_free_stream(self) -> "Stream":
        return async_to_sync(self.aget_free_stream)()  # type: ignore

    async def aget_free_stream(self) -> "Stream":
        free_stream_points = await StreamPoint.objects.afree_stream_points()  # type: ignore
        if await free_stream_points.acount() > 0:
            return await self.acreate(stream_point=await free_stream_points.afirst())  # type: ignore
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
        SENT = "SENT", _("SENT")
        UNACKNOWLEDGED = "UNACKNOWLEDGED", _("UNACKNOWLEDGED")
        FINISHED = "FINISHED", _("FINISHED")
        RECEIVED = "RECEIVED", _("RECEIVED")

        @classmethod
        def from_sc_string(cls, sc_string: str):
            """Converts a string from SuperCollider to our typed state choices.

            .. todo::

                return type
            """
            try:
                return getattr(cls, sc_string.upper())
            except AttributeError:
                log.error(f'Could not parse "{sc_string}" state to django state')
                return cls.FAILURE

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
        related_name="instructions",
        # @todo remove null
        null=True,
    )

    instruction_text = models.TextField(
        verbose_name=_("Instruction that gets transmitted via OSC"),
    )

    state = models.TextField(
        verbose_name="Instruction state",
        max_length=100,
        choices=InstructionState.choices,
        default=InstructionState.UNACKNOWLEDGED,
        editable=False,
    )

    return_value = models.TextField(
        verbose_name="Return value from statement",
        blank=True,
        default="",
        editable=False,
    )

    class Meta:
        ordering = ["-modified_date", "stream_point"]
        verbose_name = _("Stream Instruction")
        verbose_name_plural = _("Stream Instructions")

    def __str__(self) -> str:
        return f"{self.uuid} ({self.state})"


class AudioFile(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    file = models.FileField(
        editable=True,
        blank=True,
        null=True,
        upload_to="audio_files",
    )

    description = models.TextField(
        verbose_name=_("Additional description"),
        editable=True,
        blank=True,
        default="",
    )

    @classmethod
    def from_file(cls, file_content: io.BytesIO, description: str = "") -> "AudioFile":
        audio_file = cls(
            description=description,
        )
        audio_file.file = File(file_content, name=f"{audio_file.uuid}")
        audio_file.save()
        return audio_file

    class Meta:
        verbose_name = "Audio file"
        verbose_name_plural = "Audio files"

    def __str__(self) -> str:
        return f"{self.file}"


class TextToSpeech(models.Model):
    class VoiceNameChoices(models.TextChoices):
        """See `here <https://cloud.google.com/text-to-speech/docs/voices>`_.

        The first 5 characters need to be the language code
        """

        DE_STANDARD_A__FEMALE = "de-DE-Standard-A", _("de-DE-Standard-A__FEMALE")
        DE_STANDARD_B__MALE = "de-DE-Standard-B", _("de-DE-Standard-B__MALE")
        DE_STANDARD_C__FEMALE = "de-DE-Standard-C", _("de-DE-Standard-C__FEMALE")
        DE_STANDARD_D__MALE = "de-DE-Standard-D", _("de-DE-Standard-D__MALE")
        DE_STANDARD_E__MALE = "de-DE-Standard-E", _("de-DE-Standard-E__MALE")
        DE_STANDARD_F__FEMALE = "de-DE-Standard-F", _("de-DE-Standard-F__FEMALE")

        DE_WAVENET_A__FEMALE = "de-DE-Wavenet-A", _("de-DE-Wavenet-A__FEMALE")
        DE_WAVENET_B__MALE = "de-DE-Wavenet-B", _("de-DE-Wavenet-B__MALE")
        DE_WAVENET_C__FEMALE = "de-DE-Wavenet-C", _("de-DE-Wavenet-C__FEMALE")
        DE_WAVENET_D__MALE = "de-DE-Wavenet-D", _("de-DE-Wavenet-D__MALE")
        DE_WAVENET_E__MALE = "de-DE-Wavenet-E", _("de-DE-Wavenet-E__MALE")
        DE_WAVENET_F__FEMALE = "de-DE-Wavenet-F", _("de-DE-Wavenet-F__FEMALE")

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    audio_file = models.ForeignKey(
        to=AudioFile,
        on_delete=models.CASCADE,
    )

    text = models.TextField(
        verbose_name=_("Input text in SSML format"),
        editable=False,
        max_length=5000,  # limit from google API
        blank=False,
        null=False,
        default="<speak>Hallo Welt</speak>",
    )

    voice_name = models.CharField(
        max_length=64,
        verbose_name=_("Name of voice used to generate"),
        choices=VoiceNameChoices.choices,
        default=VoiceNameChoices.DE_STANDARD_D__MALE,
    )

    @classmethod
    def create_from_text(
        cls,
        ssml_text: str,
        voice_name: str = VoiceNameChoices.DE_STANDARD_D__MALE,
        force_new: bool = False,
    ) -> "TextToSpeech":
        """Copied from
        `google examples <https://cloud.google.com/text-to-speech/docs/libraries#client-libraries-install-python>`_
        """
        if not force_new:
            existing_text = cls.objects.filter(
                text=ssml_text,
            ).first()
            if existing_text:
                return existing_text

        client = texttospeech.TextToSpeechClient()

        log.info(f"Request text to speech for {ssml_text[0:100]}")
        response = client.synthesize_speech(
            input=texttospeech.SynthesisInput(
                ssml=ssml_text,
            ),
            voice=texttospeech.VoiceSelectionParams(
                language_code="de-de",
                name=voice_name,
            ),
            audio_config=texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            ),
        )
        log.debug(f"Received text to speech for {ssml_text[0:100]}")

        audio_file = AudioFile.from_file(
            file_content=io.BytesIO(response.audio_content)  # type: ignore
        )
        log.info(f"Saved audio of text {ssml_text[0:100]} to {audio_file.file.name}")
        return cls.objects.create(
            audio_file=audio_file,
            text=ssml_text,
            voice_name=voice_name,
        )

    class Meta:
        verbose_name = "Text to speech job"
        verbose_name_plural = "Text to speech jobs"

    def __str__(self) -> str:
        return f"{self.text[0:100]}"
