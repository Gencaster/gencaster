"""
Types
=====

"""

import uuid
from typing import List, Optional

import strawberry
import strawberry.django
from strawberry import auto

import stream.models as stream_models
from stream.types import AudioFile

from . import models

# @todo
# error: Cannot assign multiple types to name "CellType" without an explicit "Type[...]" annotation  [misc]
CellType = strawberry.enum(models.CellType)  # type: ignore
PlaybackType = strawberry.enum(models.AudioCell.PlaybackChoices)  # type: ignore
TemplateType = strawberry.enum(models.Graph.GraphDetailTemplate)  # type: ignore


@strawberry.input
class NodeCreate:
    name: str
    graph_uuid: uuid.UUID
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    color: Optional[str] = None


@strawberry.input
class NodeUpdate:
    uuid: uuid.UUID
    name: Optional[str] = None
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    color: Optional[str] = None


@strawberry.input
class EdgeInput:
    node_in_uuid: uuid.UUID
    node_out_uuid: uuid.UUID


@strawberry.django.filters.filter(models.Graph, lookups=True)
class GraphFilter:
    name: auto
    slug_name: auto


@strawberry.django.type(models.Graph)
class Graph:
    uuid: auto
    name: auto
    display_name: auto
    slug_name: auto
    template_name: TemplateType
    start_text: auto
    about_text: auto
    end_text: auto
    nodes: List["Node"]

    @strawberry.django.field
    def edges(self) -> List["Edge"]:
        return models.Edge.objects.filter(in_node__graph=self)  # type: ignore


@strawberry.django.type(models.Node)
class Node:
    uuid: auto
    name: auto
    color: auto
    position_x: auto
    position_y: auto
    is_entry_node: auto

    in_edges: List["Edge"]
    out_edges: List["Edge"]
    script_cells: List["ScriptCell"]


@strawberry.django.type(models.Edge)
class Edge:
    uuid: auto
    in_node: Node
    out_node: Node


@strawberry.django.type(models.AudioCell)
class AudioCell:
    uuid: auto
    playback: PlaybackType  # type: ignore
    volume: auto
    audio_file: AudioFile


@strawberry.django.type(models.ScriptCell)
class ScriptCell:
    uuid: auto
    node: Node
    cell_type: CellType  # type: ignore
    cell_code: auto
    cell_order: auto
    audio_cell: Optional[AudioCell]


@strawberry.django.input(stream_models.AudioFile, partial=True)
class AudioFileReference:
    uuid: auto


@strawberry.django.input(models.AudioCell)
class AudioCellInput:
    uuid: auto = strawberry.django.field(default=None)
    playback: PlaybackType
    audio_file: AudioFileReference
    volume: float = 0.2


@strawberry.django.input(models.ScriptCell)
class ScriptCellInput:
    uuid: auto = strawberry.django.field(default=None)
    cell_type: CellType  # type: ignore
    cell_code: auto
    cell_order: auto = strawberry.django.field(default=None)
    audio_cell: Optional[AudioCellInput]


@strawberry.django.input(models.Graph)
class AddGraphInput:
    name: auto
    display_name: auto
    slug_name: auto
    start_text: auto
    about_text: auto
    end_text: auto
    public_visible: auto
    stream_assignment_policy: auto
    template_name: TemplateType
