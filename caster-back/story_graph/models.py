import uuid

from django.db import models
from django.utils.translation import gettext as _

from stream.models import StreamPoint


class Graph(models.Model):
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

    class Meta:
        verbose_name = "Graph"
        verbose_name_plural = "Graphs"

    def __str__(self) -> str:
        return self.name


class Node(models.Model):
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

    def __str__(self) -> str:
        return f"{self.in_node} -> {self.out_node}"


class ScriptCell(models.Model):
    class CellType(models.TextChoices):
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
        unique_together = ["cell_order", "node"]
        ordering = ["node", "cell_order"]

    def __str__(self) -> str:
        return f"{self.node}-{self.cell_order} ({self.cell_type})"


class GraphSession(models.Model):
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
