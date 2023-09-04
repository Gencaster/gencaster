"""
Models
======
"""

import logging
import uuid

from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, signals
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django_stubs_ext.db.models import TypedModelMeta

from gencaster.distributor import GenCasterChannel

log = logging.getLogger(__name__)


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

    class GraphDetailTemplate(models.TextChoices):
        DEFAULT = "default", _("Default template")

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

    display_name = models.CharField(
        max_length=512,
        verbose_name=_("Display name"),
        help_text=_("Will be used as a display name in the frontend"),
    )

    slug_name = models.SlugField(
        verbose_name=_("Slug name"),
        max_length=256,
        unique=True,
        help_text=_("Will be used as a URL"),
    )

    stream_assignment_policy = models.CharField(
        max_length=255,
        help_text=_("Manages the stream assignment for this graph"),
        choices=StreamAssignmentPolicy.choices,
        default=StreamAssignmentPolicy.ONE_USER_ONE_STREAM,
    )

    public_visible = models.BooleanField(
        verbose_name=_("Public visible?"),
        help_text=_(
            "If the graph is not public it will not be listed in the frontend, yet it is still accessible via URL"
        ),
        default=True,
        null=False,
        blank=False,
    )

    template_name = models.CharField(
        max_length=255,
        verbose_name=_("Frontend template"),
        help_text=_(
            "Allows to switch to a different template in the frontend with different connection flows or UI"
        ),
        choices=GraphDetailTemplate.choices,
        default=GraphDetailTemplate.DEFAULT,
        blank=False,
        null=False,
    )

    start_text = models.TextField(
        verbose_name=_("Start text (markdown)"),
        help_text=_(
            "Text about the graph which will be displayed at the start of a stream - only if this is set"
        ),
        default="",
        blank=True,
        null=False,
    )

    about_text = models.TextField(
        verbose_name=_("About text (markdown)"),
        help_text=_(
            "Text about the graph which can be accessed during a stream - only if this is set"
        ),
        default="",
        blank=True,
        null=False,
    )

    end_text = models.TextField(
        verbose_name=_("End text (markdown)"),
        help_text=_("Text which will be displayed at the end of a stream"),
        default="",
        blank=True,
        null=False,
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

    async def aget_default_out_door(self) -> "NodeDoor":
        return await sync_to_async(self.get_default_out_door)()

    def get_default_out_door(self) -> "NodeDoor":
        default_out_door = NodeDoor.objects.filter(
            node=self,
            door_type=NodeDoor.DoorType.OUTPUT,
            is_default=True,
        ).first()
        if default_out_door is None:
            raise NodeDoorMissing(f"Default out door for node {self} is missing")
        return default_out_door

    async def aget_default_in_door(self) -> "NodeDoor":
        return await sync_to_async(self.get_default_in_door)()

    def get_default_in_door(self) -> "NodeDoor":
        default_in_door = NodeDoor.objects.filter(
            node=self,
            door_type=NodeDoor.DoorType.INPUT,
            is_default=True,
        ).first()
        if default_in_door is None:
            raise NodeDoorMissing(f"Default in door for node {self} is missing")
        return default_in_door

    def save(self, *args, **kwargs):
        create_default_doors = self._state.adding
        super().save(*args, **kwargs)
        if create_default_doors:
            for t in NodeDoor.DoorType:
                NodeDoor(
                    node=self,
                    name="default",
                    door_type=t,
                    is_default=True,
                    code="True",
                ).save()

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


class NodeDoorMissing(Exception):
    """Exception that can be thrown if a node door is missing.
    Normally each node should have a default in- and out
    :class:`~NodeDoor` via a signal, but as this is not forced
    via the database it is necessary to check for it.
    In case this check fails, this exception can be raised.
    """


class NodeDoor(models.Model):
    """A :class:`~Node` can be entered and exited via
    multiple paths, where each of these exits and
    entrances is called a *door*.

    A connection between nodes can only be made via their
    doors.
    There are two types of doors:

    .. list-table:: Door types
        :header-rows: 1

        * - Kind
          - Description
        * - **INPUT**
          - Allows to enter a node.
            Currently each Node only has one entry point
            but for future development and a nicer
            database operations it is also represented.
        * - **OUTPUT**
          - Allows to exit a node.
            After all script cells of a node has been
            executed, the condition of each door will
            be evaluated (like in a switch case).
            Once a condition has been met, the door
            will be stepped through.
            This allows to have a visual representation
            of logic branches.

    It is only possible to connect an **OUTPUT** to an
    **INPUT** door via an :class:`~Edge`.
    """

    class DoorType(models.TextChoices):
        INPUT = "input", _("Input")
        OUTPUT = "output", _("output")

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    door_type = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        choices=DoorType.choices,
        default=DoorType.OUTPUT,
    )

    node = models.ForeignKey(
        to=Node,
        on_delete=models.CASCADE,
        related_name="node_doors",
    )

    name = models.CharField(
        max_length=512,
        blank=False,
        null=False,
    )

    order = models.IntegerField(
        default=0,
    )

    is_default = models.BooleanField(
        default=False,
    )

    code = models.TextField(
        null=False,
        blank=False,
        default="",
    )

    # only here for type-hints on reverse-relations
    out_edges: models.QuerySet["Edge"]
    in_edges: models.QuerySet["Edge"]

    class Meta(TypedModelMeta):
        ordering = [
            "node",
            "is_default",
            "order",
            "name",
        ]
        verbose_name = _("Node door")
        verbose_name_plural = _("Node doors")

        constraints = [
            models.UniqueConstraint(
                fields=["node", "door_type"],
                # see https://stackoverflow.com/a/72586940
                condition=Q(is_default=True),
                name="unique_default_per_type_and_node",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.node}: {self.door_type}_{self.name}"


@receiver(signals.post_save, sender=NodeDoor, dispatch_uid="update_node_door_ws")
def update_node_door_ws(sender, instance: NodeDoor, **kwargs) -> None:
    channel_layer = get_channel_layer()
    if channel_layer is None:
        log.error(
            "Failed to obtain a handle on the channel layer to distribute node_door updates"
        )
        return
    async_to_sync(GenCasterChannel.send_node_update)(channel_layer, instance.node.uuid)
    async_to_sync(GenCasterChannel.send_graph_update)(
        channel_layer, instance.node.graph.uuid
    )


@receiver(signals.post_delete, sender=NodeDoor, dispatch_uid="delete_node_door_ws")
def delete_node_door_ws(*args, **kwargs):
    return update_node_door_ws(*args, **kwargs)


class Edge(models.Model):
    """Connects two :class:`~Node` with each other by
    using their respective :class:`~NodeDoor`.

    .. important::

        It is important to note that an edge flows from
        ``out_node_door`` to ``in_node_door`` as we follow
        the notion from the perspective of a
        :class:`story_graph.models.Node` rather than from the
        edge.


    .. graphviz::

        digraph Connection {
            rank = same;
            subgraph cluster_node_a {
                rank = same;
                label = "NODE_A";
                NODE_A [shape=Msquare, label="NODE_A\\n\\nscript_cell_1\\nscript_cell_2"];
                subgraph cluster_in_nodes_a {
                    label = "IN_NODES";
                    in_node_door_a [label="in_node_door"];
                }
                subgraph cluster_out_nodes_a {
                    label = "OUT_NODES";
                    out_node_door_a_1 [label="out_node_door 1"];
                    out_node_door_a_2 [label="out_node_door 2"];
                }
                in_node_door_a -> NODE_A [label="DB\\nreference"];
                {out_node_door_a_1, out_node_door_a_2} -> NODE_A;
                in_node_door_a -> NODE_A [style=dashed, color=red, fontcolor=red, label="Engine\\nProgression"];
                NODE_A -> out_node_door_a_1 [style=dashed, color=red];
            }

            edge_ [shape=Msquare, label="EDGE"];
            edge_ -> out_node_door_a_1 [label="out_node_door"];
            edge_ -> in_node_door_b [label="in_node_door"];
            out_node_door_a_1 -> edge_ [style=dashed, color=red];
            edge_ -> in_node_door_b [style=dashed, color=red];

            subgraph cluster_node_b {
                rank = same;
                label = "NODE_B";
                NODE_B [shape=Msquare];
                subgraph cluster_in_nodes_b {
                    label = "IN_NODES";
                    in_node_door_b [label="in_node_door"];
                }
                subgraph cluster_out_nodes_b {
                    label = "OUT_NODES";
                    out_node_door_b_1 [label="out_node_door 1"];
                    out_node_door_b_2 [label="out_node_door 2"];
                }
                in_node_door_b -> NODE_B;
                {out_node_door_b_1, out_node_door_b_2} -> NODE_B;
                in_node_door_b -> NODE_B [style=dashed, color=red];
                NODE_B -> out_node_door_b_1 [style=dashed, color=red];
            }
        }
    """

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    in_node_door = models.ForeignKey(
        NodeDoor,
        related_name="in_edges",
        on_delete=models.CASCADE,
        # this should not be none but as we
        # added it during the lifecycle of
        # gencaster it is optional as otherwise
        # all prior data has to be deleted
        null=True,
    )

    out_node_door = models.ForeignKey(
        NodeDoor,
        related_name="out_edges",
        on_delete=models.CASCADE,
        # see in_node_door
        null=True,
    )

    def save(self, *args, **kwargs):
        """Checks if ``in_node_door`` and ``out_node_door`` have their
        respective types in order to avoid any *wrong* directions within
        our graph.
        """
        if self.in_node_door:
            if self.in_node_door.door_type != NodeDoor.DoorType.INPUT:
                raise ValidationError(_("in_node_door needs to be an input door"))
        if self.out_node_door:
            if self.out_node_door.door_type != NodeDoor.DoorType.OUTPUT:
                raise ValidationError(_("out_node_door needs to be an output door"))
        super().save(*args, **kwargs)

    class Meta(TypedModelMeta):
        constraints = [
            models.UniqueConstraint(
                fields=["in_node_door", "out_node_door"],
                name="unique_edge",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.in_node_door} -> {self.out_node_door}"


class AudioCell(models.Model):
    """Stores information for playback of static audio files."""

    class PlaybackChoices(models.TextChoices):
        """Different kinds of playback.

        .. list-table:: Playback types
            :header-rows: 1

            * - Name
              - Description
            * - ``SYNC``
              - Plays back an audio file and waits for the
                playback to finish before continuing the
                execution of the script cells.
            * - ``ASYNC``
              - Plays back an audio file and immediately
                continues the execution of script cells.
                This is fitting for e.g. background music.
        """

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
    """A :class:`~story_graph.models.ScriptCell` can contain
    different types of code, each with unique functionality.

    Both, the database and :class:`~story_graph.engine.Engine`,
    implement some specific details according to these types.

    .. list-table:: Cell types
        :header-rows: 1

        * - Name
          - Description
          - Database
          - Engine
        * - Markdown
          - Allows to write arbitrary text which will get
            rendered as an audio file via a text to speech service,
            see :class:`~stream.models.TextToSpeech` for conversion
            and :class:`~story_graph.markdown_parser.GencasterRenderer`
            for the extended Markdown syntax.
          - - :class:`~stream.models.TextToSpeech`
          - - :func:`~story_graph.engine.Engine.execute_markdown_code`
            - :class:`~story_graph.markdown_parser.GencasterRenderer`
        * - Python
          - Allows to execute python code via :func:`exec` which allows
            to trigger e.g. Dialogs in the frontend
            (see :class:`~stream.frontend_types.Dialog`)
            or calculate or fetch any kind of data and store its value
            as a :class:`~stream.models.StreamVariable`.
          -
          - - :func:`~story_graph.engine.Engine.execute_python_cell`
        * - SuperCollider
          - Executes *sclang* code on the associated server.
            This can be used to control the sonic content on the server.
          - - :class:`~stream.models.StreamInstruction`
          - - :func:`~story_graph.engine.Engine.execute_sc_code`
            - :ref:`OSC Server`
        * - Comment
          - Does not get executed, but allows to put comments into
            the graph.
          -
          -
        * - Audio
          - Allows to playback static audio files.
            The instruction will be translated into *sclang* code and will
            be executed as such on the associated stream.
          - - :class:`~story_graph.models.AudioCell`
            - :class:`~stream.models.AudioFile`
          - - :func:`~story_graph.engine.Engine.execute_audio_cell`

    """

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
