"""
Models
======
"""

import uuid
from typing import Optional

from django.db import models
from django.utils.translation import gettext as _

from stream.models import StreamPoint


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

    async def get_entry_node(self) -> Optional["Node"]:
        # @todo need to return the "Main" node
        # which shall be our entry node
        return await self.nodes.afirst()  # type: ignore

    class Meta:
        verbose_name = "Graph"
        verbose_name_plural = "Graphs"

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

    class Meta:
        ordering = ["graph"]

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


class ScriptCell(models.Model):
    """Stores a script which can be executed
    with our :class:`~story_graph.engine.Engine` on a
    :class:`~stream.models.Stream`.
    """

    class CellType(models.TextChoices):
        """Choice of foobar"""

        MARKDOWN = ["markdown", _("Markdown")]
        PYTHON = ["python", _("Python")]
        SUPERCOLLIDER = ["supercollider", _("SuperCollider")]
        COMMENT = ["comment", _("Comment")]

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

    class Meta:
        # ordering by uuid provides a deterministic order
        # in case cell_order is not unique
        ordering = ["node", "cell_order", "uuid"]

    def __str__(self) -> str:
        return f"{self.node}-{self.cell_order} ({self.cell_type})"


class GraphSession(models.Model):
    """A stroy session.

    .. todo::

        Do we need this?

    """

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        unique=True,
    )

    graph = models.ForeignKey(
        Graph,
        related_name="graph_sessions",
        on_delete=models.CASCADE,
    )

    streaming_point = models.ForeignKey(
        StreamPoint,
        related_name="graph_sessions",
        on_delete=models.CASCADE,
    )
