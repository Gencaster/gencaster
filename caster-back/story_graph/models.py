"""
Models
======
"""

import uuid

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _


class Graph(models.Model):
    """A collection of :class:`~Node` and :class:`~Edge`.
    This can be considered a score as well as a program as it
    has an entry point as a :class:`~Node` and can jump to any
    other :class:`~Node`, also allowing for recursive loops/cycles.

    Each node can be considered a little program on its own which can consist
    of multiple :class:`~ScriptCell` which can be coded in a variety of
    languages which can control the frontend and the audio (by e.g. speaking
    on the stream) or setting a background music.

    The story graph is a core concept and can be edited with a native editor.
    """

    class StreamAssignmentPolicy(models.TextChoices):
        ONE_GRAPH_ONE_STREAM = "one_graph_one_stream", _(
            "Each graph has only one stream"
        )
        ONE_USER_ONE_STREAM = "one_user_one_stream", _("Each user gets its own stream")
        DEACTIVATE = "deactivate", _("No stream assignment")

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Name of the graph"),
        unique=True,
    )

    stream_assignment_policy = models.CharField(
        max_length=255,
        help_text=_("Manages the stream assignment for this graph"),
        choices=StreamAssignmentPolicy.choices,
        default=StreamAssignmentPolicy.ONE_USER_ONE_STREAM,
    )

    async def aget_entry_node(self) -> "Node":
        """
        See :func:`Graph.create_entry_node`.
        """
        return await Node.objects.aget(is_entry_node=True, graph=self)

    async def acreate_entry_node(self) -> "Node":
        """
        Every graph needs a deterministic, unique entry node which is used
        to start the iteration over the graph.

        The creator of the graph is responsible for calling this method
        as we can not implicit call it because there are a multitude of
        ways of creating a Graph (async (asave), sync (save) or in a bulk where
        we do not have a handle at all).
        """
        return await Node.objects.acreate(
            is_entry_node=True,
            graph=self,
            name="Start",
        )

    class Meta:
        verbose_name = "Graph"
        verbose_name_plural = "Graphs"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Node(models.Model):
    """
    A node.
    """

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Name of the node"),
        default="",
    )

    color = models.CharField(
        verbose_name=_("HEX color of the node in graph canvas"),
        max_length=16,
        default="#fff",
    )

    position_x = models.FloatField(
        help_text=_("x-Position in graph canvas"),
        default=0.0,
    )

    position_y = models.FloatField(
        help_text=_("y-Position in graph canvas"),
        default=0.0,
    )

    graph = models.ForeignKey(
        Graph,
        related_name="nodes",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    is_entry_node = models.BooleanField(
        verbose_name="Is Entry node?",
        help_text=_(
            "Acts as a singular entrypoint for our graph."
            "Only one such node can exist per graph."
        ),
        default=False,
    )

    is_blocking_node = models.BooleanField(
        verbose_name="Is blocking node?",
        help_text=_(
            "If we encounter this node during graph execution we will halt execution indefinitely on this node. This is useful if we have setup a state and do not want to change it anymore."
        ),
        default=False,
    )

    class Meta:
        ordering = ["graph"]
        constraints = [
            models.UniqueConstraint(
                fields=["graph"],
                condition=Q(is_entry_node=True),
                name="unique_entry_point",
            )
        ]

    def __str__(self) -> str:
        return self.name


class Edge(models.Model):
    """Connects two :class:`~Node` with each other.

    .. todo::

        With a script we can also jump to any other node
        so it is not clear how to use this.
        Maybe take a look at visual programming languages
        such as MSP or Scratch how they handle this?
    """

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    in_node = models.ForeignKey(
        Node,
        related_name="out_edges",
        on_delete=models.CASCADE,
    )

    out_node = models.ForeignKey(
        Node,
        related_name="in_edges",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["in_node", "out_node"],
                name="unique_edge",
            )
        ]

    def __str__(self) -> str:
        return f"{self.in_node} -> {self.out_node}"


class AudioCell(models.Model):
    class PlaybackChoices(models.TextChoices):
        SYNC_PLAYBACK = ["sync_playback", _("Sync playback")]
        ASYNC_PLAYBACK = ["async_playback", _("Async playback")]

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    playback = models.CharField(
        max_length=512,
        choices=PlaybackChoices.choices,
        default=PlaybackChoices.SYNC_PLAYBACK,
        null=False,
        blank=False,
    )

    audio_file = models.ForeignKey(
        "stream.AudioFile",
        on_delete=models.CASCADE,
        related_name="audio_cells",
        null=False,
        blank=False,
    )

    volume = models.FloatField(
        default=0.2,
    )

    def __str__(self) -> str:
        return f"{self.audio_file} ({self.playback})"


class CellType(models.TextChoices):
    """Choice of foobar"""

    MARKDOWN = ["markdown", _("Markdown")]
    PYTHON = ["python", _("Python")]
    SUPERCOLLIDER = ["supercollider", _("SuperCollider")]
    COMMENT = ["comment", _("Comment")]
    AUDIO = ["audio", _("Audio")]


class ScriptCell(models.Model):
    """Stores a script which can be executed
    with our :class:`~story_graph.engine.Engine` on a
    :class:`~stream.models.Stream`.
    """

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    node = models.ForeignKey(
        Node,
        related_name="script_cells",
        on_delete=models.CASCADE,
    )

    cell_type = models.CharField(
        max_length=128,
        choices=CellType.choices,
        default=CellType.COMMENT,
        verbose_name=_("Cell type"),
        null=False,
        blank=False,
    )

    cell_code = models.TextField(
        verbose_name=_("Cell code"),
    )

    cell_order = models.IntegerField(
        default=0,
    )

    audio_cell = models.OneToOneField(
        AudioCell,
        on_delete=models.CASCADE,
        related_name="script_cell",
        null=True,
        blank=True,
    )

    class Meta:
        # ordering by uuid provides a deterministic order
        # in case cell_order is not unique
        ordering = ["node", "cell_order", "uuid"]
        constraints = [
            models.CheckConstraint(
                check=Q(cell_type=CellType.AUDIO, audio_cell__isnull=False)
                | ~Q(cell_type=CellType.AUDIO),
                name="audio_type_needs_audio_cell_information",
            )
        ]

    def __str__(self) -> str:
        return f"{self.node}-{self.cell_order} ({self.cell_type})"
