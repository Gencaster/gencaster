import uuid
from io import BytesIO
import logging

from google.cloud import texttospeech
from django.db import models
from django.utils.translation import gettext as _
from django.core.files import File
from django.contrib import admin

log = logging.getLogger(__file__)


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

    audio_file = models.FileField(
        editable=False, blank=True, null=True, upload_to="speech_to_text/"
    )

    def generate_sound_file(self):
        """Copied from
        `google examples <https://cloud.google.com/text-to-speech/docs/libraries#client-libraries-install-python>`_
        """
        client = texttospeech.TextToSpeechClient()

        log.info(f"Request text to speech on {self.uuid}")
        response = client.synthesize_speech(
            input=texttospeech.SynthesisInput(
                ssml=self.text,
            ),
            voice=texttospeech.VoiceSelectionParams(
                language_code="de-de",
                name=self.voice_name,
            ),
            audio_config=texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            ),
        )

        self.audio_file = File(
            BytesIO(response.audio_content),
            name=f"{self.uuid}.wav",
        )
        self.save()
        log.info("Saved text to speech for {self.uuid} under {self.audio_file.path}")

    class Meta:
        verbose_name = "Text to speech job"
        verbose_name_plural = "Text to speech jobs"

    def __str__(self) -> str:
        return f"{self.uuid}"
