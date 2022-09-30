from typing import List

import strawberry
import strawberry.django
from strawberry import auto

from . import models


@strawberry.django.type(models.Graph)
class Graph:
    uuid: auto
    name: auto
    nodes: List["Node"]


@strawberry.django.type(models.Node)
class Node:
    uuid: auto
    name: auto
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
