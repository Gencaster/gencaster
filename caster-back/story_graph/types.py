"""
Types
=====

"""

import uuid
from typing import List, Optional

import strawberry
import strawberry.django
from strawberry import auto

from . import models

CellType = strawberry.enum(models.ScriptCell.CellType)


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


@strawberry.django.type(models.Graph)
class Graph:
    uuid: auto
    name: auto
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


@strawberry.django.type(models.GraphSession)
class GraphSession:
    uuid: auto
    graph: Graph


@strawberry.django.type(models.ScriptCell)
class ScriptCell:
    uuid: auto
    node: Node
    cell_type: CellType  # type: ignore
    cell_code: auto
    cell_order: auto


@strawberry.django.input(models.ScriptCell)
class ScriptCellInput:
    uuid: auto
    cell_type: CellType  # type: ignore
    cell_code: auto
    cell_order: auto


@strawberry.django.input(models.ScriptCell)
class NewScriptCellInput:
    # same as ScriptCellInput but on creation we hand out the UUID
    cell_type: CellType  # type: ignore
    cell_code: auto
    cell_order: auto
