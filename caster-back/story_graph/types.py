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
NodeDoorType = strawberry.enum(models.NodeDoor.DoorType)  # type: ignore


def create_python_highlight_string(e: SyntaxError) -> str:
    """Creates from a given error a string which highlights
    the error, so it will return for example

        foo++
             ^

    """
    if not (e.text and e.lineno and e.offset and e.end_offset):
        raise Exception(f"Missing syntax error information {e}")
    t = e.text.split("\n")
    patch = [" "] * e.end_offset
    patch[max(e.offset - 1, 0) : max(e.end_offset - 1, 0)] = "^"
    t.insert(e.lineno, "".join(patch))
    return "\n".join(t)


@strawberry.type
class InvalidPythonCode:
    error_type: str
    error_message: str
    error_code: str


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
    node_door_in_uuid: uuid.UUID
    node_door_out_uuid: uuid.UUID


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
        return models.Edge.objects.filter(out_node_door__node__graph=self)  # type: ignore


@strawberry.django.type(models.Node)
class Node:
    uuid: auto
    name: auto
    color: auto
    position_x: auto
    position_y: auto
    is_entry_node: auto

    script_cells: List["ScriptCell"]
    node_doors: List["NodeDoor"]

    @strawberry.django.field
    def in_node_doors(self) -> List["NodeDoor"]:
        return models.NodeDoor.objects.filter(
            node=self,
            door_type=models.NodeDoor.DoorType.INPUT,
        )  # type: ignore

    @strawberry.django.field
    def out_node_doors(self) -> List["NodeDoor"]:
        return models.NodeDoor.objects.filter(
            node=self,
            door_type=models.NodeDoor.DoorType.OUTPUT,
        )  # type: ignore


@strawberry.django.type(models.NodeDoor)
class NodeDoor:
    uuid: auto
    door_type: NodeDoorType  # type: ignore
    node: Node
    name: auto
    order: auto
    is_default: auto
    code: auto


@strawberry.django.input(models.NodeDoor)
class NodeDoorInputCreate:
    # default is disabled as it is not possible for a user
    # to create a default door
    door_type: NodeDoorType  # type: ignore
    name: auto
    order: auto
    code: auto


# @strawberry.django.input(models.NodeDoor) - using this makes
# some mandatory fields optional - so we use a manual setup
@strawberry.input
class NodeDoorInputUpdate:
    uuid: uuid.UUID
    door_type: NodeDoorType = models.NodeDoor.DoorType.OUTPUT  # type: ignore
    name: Optional[str] = None
    order: Optional[int] = None
    code: Optional[str] = None


NodeDoorResponse = strawberry.union("NodeDoorResponse", [NodeDoor, InvalidPythonCode])


@strawberry.django.type(models.Edge)
class Edge:
    uuid: auto
    in_node_door: NodeDoor
    out_node_door: NodeDoor


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
class ScriptCellInputCreate:
    cell_type: CellType  # type: ignore
    cell_code: auto
    cell_order: auto = strawberry.django.field(default=None)
    audio_cell: Optional[AudioCellInput]


@strawberry.django.input(models.ScriptCell)
class ScriptCellInputUpdate:
    uuid: auto = uuid.UUID
    cell_type: Optional[CellType]  # type: ignore
    cell_code: Optional[str]
    cell_order: Optional[int]
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
