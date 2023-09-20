import io
import logging
import uuid
from datetime import timedelta
from typing import Optional

from asgiref.sync import async_to_sync
from django.conf import settings
from django.contrib import admin
from django.core.files import File
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext as _
from google.cloud import texttospeech
from pythonosc.udp_client import SimpleUDPClient

import story_graph.models
from gencaster.distributor import GenCasterChannel

from .exceptions import NoStreamAvailableException

log = logging.getLogger(__name__)


class StreamPointManager(models.Manager["StreamPoint"]):
    def free_stream_points(self) -> models.QuerySet["StreamPoint"]:
        return async_to_sync(self.afree_stream_points)()  # type: ignore

    async def afree_stream_points(self) -> models.QuerySet["StreamPoint"]:
        return self.exclude(streams__num_listeners__gt=0).filter(
            last_live__gt=timezone.now()
            - timedelta(seconds=settings.STREAM_MAX_BEACON_SEC)
        )


class StreamPoint(models.Model):
    """Stores metadata for each SuperCollider/Janus instance
    and how we can interact with this instance.

    Every SuperCollider instance that send a beacon to us
    via the :ref:`OSC Server` will be a StreamPoint.
    Consider ``last_live`` to filter out non-live from live
    instances.
    """

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

    def speak_on_stream(self, ssml_text: str) -> "StreamInstruction":
        """Speaks on the stream

        :param ssml_text: See https://cloud.google.com/text-to-speech/docs/ssml
        """
        tts = TextToSpeech.create_from_text(ssml_text)
        return self.play_audio_file(
            tts.audio_file,
            playback_type=story_graph.models.AudioCell.PlaybackChoices.SYNC_PLAYBACK,
        )

    def play_audio_file(
        self,
        audio_file: "AudioFile",
        playback_type: story_graph.models.AudioCell.PlaybackChoices = story_graph.models.AudioCell.PlaybackChoices.ASYNC_PLAYBACK,
    ) -> "StreamInstruction":
        sc_audio_file_path = f"/data/{audio_file.file.name}"

        manual_finish = False

        if playback_type == story_graph.models.AudioCell.PlaybackChoices.ASYNC_PLAYBACK:
            instruction = StreamInstruction.objects.create(
                stream_point=self,
                instruction_text=f'{{g.playBuffer("{sc_audio_file_path}")}}',
            )
        elif (
            playback_type == story_graph.models.AudioCell.PlaybackChoices.SYNC_PLAYBACK
        ):
            manual_finish = True
            # we need the uuid on the finish message so we first create the instruction
            # and after it we modify the callback to include its UUID
            # @todo: another idea: store the UUID on the Gencsater server instance
            # of supercollider, but this could be overwritten by another instruction?
            instruction = StreamInstruction.objects.create(
                stream_point=self, instruction_text=""
            )
            instruction.instruction_text = (
                f'{{g.syncPlayBuffer("{sc_audio_file_path}", "{instruction.uuid}")}}'
            )
            instruction.save()
        else:
            raise NotImplementedError(f"Unsupported playback type {playback_type}")

        self.send_stream_instruction(instruction, manual_finish)
        return instruction

    # todo make this async?
    def send_raw_instruction(self, instruction_text: str) -> "StreamInstruction":
        instruction: StreamInstruction = StreamInstruction.objects.create(
            stream_point=self,
            instruction_text=instruction_text,
        )
        self.send_stream_instruction(instruction)
        return instruction

    def send_stream_instruction(
        self, instruction: "StreamInstruction", manual_finish: bool = False
    ) -> None:
        """Sends an OSC message with an instruction to our SuperCollider server.
        Check the function `instructionReceiver` in `GenCaster.sc` which will accept the send message.

        :param instruction: The given instruction on the Server.
        :param manual_finish: If set to True, one has to take care self of sending the unlocking `finished` message.
            This is helpful in cases of async function calls, e.g. on a playback of a sample.
            Defaults to False.
        """
        self.client.send_message(
            address="/instruction",
            value=[str(instruction.uuid), instruction.instruction_text, manual_finish],
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
    def get_free_stream(self, graph: "story_graph.models.Graph") -> "Stream":
        return async_to_sync(self.aget_free_stream)(graph)  # type: ignore

    async def aget_free_stream(self, graph: "story_graph.models.Graph") -> "Stream":
        """
        Tries to obtain a stream by obey the stream assignment policy of the Graph.
        """
        # avoid circular dependency
        from story_graph.models import Graph

        if (
            graph is not None
            and graph.stream_assignment_policy
            == Graph.StreamAssignmentPolicy.ONE_GRAPH_ONE_STREAM
        ):
            existing_stream: Optional[Stream] = (
                await Stream.objects.filter(num_listeners__gt=0, graph=graph)
                .prefetch_related("stream_point")
                .afirst()
            )
            if existing_stream:
                return existing_stream

        free_stream_points = await StreamPoint.objects.afree_stream_points()  # type: ignore
        if await free_stream_points.acount() == 0:
            raise NoStreamAvailableException()
        stream: Stream = await self.acreate(
            stream_point=await free_stream_points.afirst(),
            graph=graph,
        )  # type: ignore

        return stream

    def disconnect_all_streams(self):
        stream: Stream
        for stream in Stream.objects.filter(num_listeners__gt=0):
            stream.disconnect()


class Stream(models.Model):
    """Assigns a :class:`~StreamPoint` to a user/client.
    This allows us to see which streams are currently in use
    and also by which user.
    It also allows us to trace past streams.
    """

    objects: StreamManager = StreamManager()

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

    num_listeners = models.IntegerField(
        default=0,
        verbose_name=_("Number of listeners"),
        help_text=_(
            "Used as a garbage collection. If multiple users share the same stream "
            "we need to know when we can release the stream which happens if listener counter is 0. "
            "It starts with a default of 0 because this allows us to count stateless."
        ),
    )

    graph = models.ForeignKey(
        "story_graph.Graph",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    async def increment_num_listeners(self):
        log.debug("Increment number of listeners")
        self.num_listeners = self.num_listeners + 1
        await self.asave()
        # await Stream.objects.filter(uuid=self.uuid).aupdate(
        #     num_listeners=F("num_listeners") + 1
        # )

    async def decrement_num_listeners(self):
        log.debug("Decrement number of listeners")
        self.num_listeners = self.num_listeners - 1
        await self.asave()
        # await Stream.objects.filter(uuid=self.uuid).aupdate(
        #     num_listeners=F("num_listeners") - 1
        # )

    def disconnect(self):
        log.info(f"Disconnect stream {self.uuid}")
        self.num_listeners = 0
        self.save()

    class Meta:
        ordering = ["-created_date", "stream_point"]
        verbose_name = _("Stream")
        verbose_name_plural = _("Streams")

    def __str__(self) -> str:
        return f"Stream on {self.stream_point}"


@receiver(signals.post_save, sender=Stream, dispatch_uid="update_streams_ws")
def update_streams_ws(sender, instance: Stream, **kwargs):
    async_to_sync(GenCasterChannel.send_streams_update)(str(instance.uuid))


class StreamVariable(models.Model):
    """Allows to store variables in a stream session as a key/value pair.

    .. warning::

        Due to database constraints all keys and values will be stored
        as a string, so parsing a float, int or boolean requires
        type conversion.

    """

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    stream = models.ForeignKey(
        Stream, on_delete=models.CASCADE, related_name="variables"
    )

    key = models.CharField(
        max_length=512,
        null=False,
        blank=False,
    )

    value = models.TextField(
        default="",
    )

    stream_to_sc = models.BooleanField(
        default=False,
        verbose_name=_("Stream to SuperCollider"),
        help_text=_("Stream values to SC as control rate Ndef"),
    )

    def send_to_sc(self) -> "StreamInstruction":
        """Makes the stream variable available on the scsynth server under the same name as an Ndef.

        .. note::

            This used to be solved with

            .. code-block:: supercollider

                Ndef(\\foo, {val});

            but this introduced a clicking noise on each update.
            The solution seems to be to use instead

            .. code-block:: supercollider

                Ndef(\\foo, val);

            without the surrounding curly brackets for the value.
        """
        return self.stream.stream_point.send_raw_instruction(
            instruction_text=f'Ndef("{self.key}".asSymbol, {self.value});'
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["stream", "key"], name="unique key within graph session"
            )
        ]

    def __str__(self) -> str:
        return f"{self.stream}: {self.key} -> {self.value}"


class StreamInstruction(models.Model):
    """Instruction for a :class:`StreamPoint`, most likely to be
    created from a :class:`~story_graph.models.ScriptCell`.
    """

    class InstructionState(models.TextChoices):
        """Possible states of our instruction.

        .. seealso::

            See also :ref:`OSC acknowledge message`.

        """

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
    """Represents a local audio file on the server.
    As SuperCollider and Django are running on the same server we
    can pass these files to the SuperCollider instances as they
    are mounted within each service.
    """

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    name = models.CharField(
        max_length=1024,
        default="untitled",
        null=False,
        blank=False,
        help_text=_("Acts as an identifier for humans"),
    )

    auto_generated = models.BooleanField(
        default=True,
        help_text=_(
            "Allows to separate automatic generated audio files speech to text and user uploads"
        ),
    )

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
    """Handles the conversion of text to speech
    by using external APIs.
    """

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

        DE_NEURAL2_B__MALE = "de-DE-Neural2-B", _("de-DE-Neural2-B__MALE")
        DE_NEURAL2_C__FEMALE = "de-DE-Neural2-C", _("de-DE-Neural2-C__FEMALE")
        DE_NEURAL2_D__MALE = "de-DE-Neural2-D", _("de-DE-Neural2-D__MALE")
        DE_NEURAL2_F__FEMALE = "de-DE-Neural2-F", _("de-DE-Neural2-F__FEMALE")

        DE_POLYGLOT_1__MALE = "de-DE-Polyglot-1", _("de-DE-Polyglot-1__MALE")

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
        default=VoiceNameChoices.DE_NEURAL2_C__FEMALE,
    )

    @classmethod
    def create_from_text(
        cls,
        ssml_text: str,
        voice_name: str = VoiceNameChoices.DE_NEURAL2_C__FEMALE,
        force_new: bool = False,
    ) -> "TextToSpeech":
        """
        Creates a new instance for a given text by calling the Google Cloud.
        We will not call the API if we find the exact same text in our database,
        in which case we will return the object from the database.
        This caching behavior can be controlled via ``force_new``.

        .. seealso::

            Copied from
            `google examples <https://cloud.google.com/text-to-speech/docs/libraries#client-libraries-install-python>`_


        :param ssml_text: SSML text to convert to audio
        :param voice_name: Voice name to use
        :param force_new: If new we will not search for existing objects
            with the same text.
        """
        if not force_new:
            if existing_text := cls.objects.filter(
                text=ssml_text,
                voice_name=voice_name,
            ).first():
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


class StreamLog(models.Model):
    class LogLevel(models.IntegerChoices):
        """Taken from ``logging`` module but omitting ``FATAL`` and ``WARN``."""

        CRITICAL = 50, _("Critical")
        ERROR = 40, _("Error")
        WARNING = 30, _("Warning")
        INFO = 20, _("Info")
        DEBUG = 10, _("Debug")
        NOTSET = 0, _("Not set")

    class Origin(models.TextChoices):
        """States from which module the current logging occurs"""

        GRAPH_ENGINE = "graph_engine", _("Graph engine")
        SUPERCOLLIDER = "supercollider", _("SuperCollider")
        JANUS = "janus", _("Janus")

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    stream_point = models.ForeignKey(
        StreamPoint,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    stream = models.ForeignKey(
        Stream,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    origin = models.TextField(
        choices=Origin.choices,
        blank=True,
        null=True,
    )

    level = models.IntegerField(
        choices=LogLevel.choices,
        default=LogLevel.INFO,
    )

    message = models.TextField(
        blank=True,
        null=False,
    )

    name = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_date"]
        verbose_name = _("Stream log")
        verbose_name_plural = _("Stream logs")

    def __str__(self) -> str:
        return f"Stream log {self.uuid}"
