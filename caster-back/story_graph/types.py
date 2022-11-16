import uuid
from typing import List, Optional

import strawberry
import strawberry.django
from strawberry import auto

from . import models


@strawberry.input
class NodeInput:
    name: str
    graph_uuid: uuid.UUID
    position_x: Optional[float]
    position_y: Optional[float]
    color: Optional[str]
    # script_cells: List["ScriptCell"]


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
        return models.Edge.objects.filter(in_node__graph=self)


@strawberry.django.type(models.Node)
class Node:
    uuid: auto
    name: auto
    color: auto
    position_x: auto
    position_y: auto

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
    cell_type: auto
    cell_code: auto
    cell_order: auto
