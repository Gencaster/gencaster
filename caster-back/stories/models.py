import uuid

from django.db import models
from django.utils.translation import gettext as _


class Story(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )
    active = models.BooleanField(default=True)

    name = models.CharField(max_length=256)
    slug = models.SlugField()

    class Meta:
        verbose_name = _("Story")
        verbose_name_plural = _("Stories")

    def __str__(self) -> str:
        return f"{self.name}"


class Chapter(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )
    active = models.BooleanField(default=True)

    name = models.CharField(max_length=256)
    slug = models.SlugField()

    story = models.ForeignKey(
        "stories.Story",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = _("Chapter")
        verbose_name_plural = _("Chapters")

    def __str__(self) -> str:
        return f"{self.story} - {self.name}"


class Block(models.Model):
    class BlockTypes(models.TextChoices):
        PREPRODUCED = "preproduced", _("Pre-Produced")
        DYNAMIC = "dynamic", _("Dynamic")
        SPECIAL = "special", _("Special")

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )
    active = models.BooleanField(default=True)

    name = models.CharField(max_length=256)
    slug = models.SlugField()

    block_type = models.CharField(
        max_length=64,
        choices=BlockTypes.choices,
    )

    chapter = models.ForeignKey(
        "stories.Chapter",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    text = models.TextField()

    audio_file = models.FileField(upload_to="audio/blocks/")

    class Meta:
        verbose_name = _("Block")
        verbose_name_plural = _("Blocks")

    def __str__(self) -> str:
        return f"{self.chapter} - {self.name}"
