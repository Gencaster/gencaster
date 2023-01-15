"""
Schema
======

Here we define all the endpoints for GraphQL.

For a specific details of the types consider the
`GraphiQL <https://github.com/graphql/graphiql>`_
page available under the `/graphql` endpoint of
the running backend.
"""

import uuid
from typing import List

import strawberry
import strawberry.django
from asgiref.sync import sync_to_async
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http.request import HttpRequest
from strawberry.types import Info
from strawberry_django.fields.field import StrawberryDjangoField

import story_graph.models as story_graph_models
from story_graph.types import (
    EdgeInput,
    Graph,
    NewScriptCellInput,
    Node,
    NodeCreate,
    NodeUpdate,
    ScriptCell,
    ScriptCellInput,
)
from stream.types import StreamPoint


class AuthStrawberryDjangoField(StrawberryDjangoField):
    """Allows us to restrict certain actions to logged in users."""

    def resolver(self, info: Info, source, **kwargs):
        request: HttpRequest = info.context.request
        if not request.user.is_authenticated:
            raise PermissionDenied()
        return super().resolver(info, source, **kwargs)


async def graphql_check_authenticated(info: Info):
    """Helper function to determine if we are loggin in an async manner.

    This would be better a decorator but strawberry is not nice in these regards, see
    `Stack Overflow <https://stackoverflow.com/a/72796313/3475778>`_.
    """
    auth = await sync_to_async(lambda: info.context.request.user.is_authenticated)()
    if auth is False:
        raise PermissionDenied()


def _update_cells(new_cells: List[ScriptCellInput]):
    with transaction.atomic():
        for new_cell in new_cells:
            story_graph_models.ScriptCell.objects.filter(uuid=new_cell.uuid).update(
                cell_order=new_cell.cell_order,
                cell_code=new_cell.cell_code,
                cell_type=new_cell.cell_type,
            )


@strawberry.type
class Query:
    """Queries for GenCaster."""

    stream_point: StreamPoint = AuthStrawberryDjangoField()
    stream_points: List[StreamPoint] = AuthStrawberryDjangoField()
    graphs: List[Graph] = AuthStrawberryDjangoField()
    graph: Graph = AuthStrawberryDjangoField()
    nodes: List[Node] = AuthStrawberryDjangoField()
    node: Node = AuthStrawberryDjangoField()


@strawberry.type
class Mutation:
    """Mutations for GenCaster via GraphQL."""

    @strawberry.mutation
    async def add_node(self, info: Info, new_node: NodeCreate) -> None:
        """Creates a new :class:`~story_graph.models.Node` in a given
        ~class:`~story_graph.models.Graph`.
        Although it creates a new node with UUID we don't hand it back yet.
        """
        await graphql_check_authenticated(info)

        graph = await sync_to_async(story_graph_models.Graph.objects.get)(
            uuid=new_node.graph_uuid
        )
        node = story_graph_models.Node(
            name=new_node.name,
            graph=graph,
        )

        # transfer from new_node to node model if attribute is not none
        for field in ["position_x", "position_y", "color"]:
            if new_value := getattr(new_node, field):
                setattr(node, field, new_value)

        await sync_to_async(node.save)()

        return None

    @strawberry.mutation
    async def update_node(self, info: Info, node_update: NodeUpdate) -> None:
        """Updates a given :class:`~story_graph.models.Node` which can be used
        for renaming or moving it across the canvas.
        """
        await graphql_check_authenticated(info)

        node = await story_graph_models.Node.objects.aget(uuid=node_update.uuid)

        for field in ["position_x", "position_y", "color", "name"]:
            if new_value := getattr(node_update, field):
                setattr(node, field, new_value)

        await sync_to_async(node.save)()

        return None

    @strawberry.mutation
    async def add_edge(self, info: Info, new_edge: EdgeInput) -> None:
        """Creates a :class:`~story_graph.models.Edge` for a given
        :class:`~story_graph.models.Graph`.
        It does not return the created edge.
        """
        await graphql_check_authenticated(info)
        in_node: story_graph_models.Node = await sync_to_async(
            story_graph_models.Node.objects.get
        )(uuid=new_edge.node_in_uuid)
        out_node: story_graph_models.Node = await sync_to_async(
            story_graph_models.Node.objects.get
        )(uuid=new_edge.node_out_uuid)
        edge: story_graph_models.Edge = await sync_to_async(
            story_graph_models.Edge.objects.create
        )(
            in_node=in_node,
            out_node=out_node,
        )
        return None

    @strawberry.mutation
    async def delete_edge(self, info, edge_uuid: uuid.UUID) -> None:
        """Deletes a given :class:`~story_graph.models.Edge`."""
        await graphql_check_authenticated(info)
        try:
            edge = await sync_to_async(story_graph_models.Edge.objects.get)(
                uuid=edge_uuid
            )
            await sync_to_async(edge.delete)()
        except Exception:
            raise Exception(f"Could not delete edge {edge_uuid}")
        return None

    @strawberry.mutation
    async def delete_node(self, info, node_uuid: uuid.UUID) -> None:
        """Deletes a given :class:`~story_graph.models.Node`."""
        await graphql_check_authenticated(info)
        try:
            node = await sync_to_async(story_graph_models.Node.objects.get)(
                uuid=node_uuid
            )
            await sync_to_async(node.delete)()
        except Exception:
            raise Exception(f"Could delete node {node_uuid}")
        return None

    @strawberry.mutation
    async def add_script_cell(
        self,
        info,
        node_uuid: uuid.UUID,
        new_script_cell: NewScriptCellInput,
    ) -> ScriptCell:
        """Creates a new :class:`~story_graph.models.ScriptCell` for a given
        :class:`~story_graph.models.Edge` and returns this cell.
        """
        await graphql_check_authenticated(info)
        try:
            node: story_graph_models.Node = await story_graph_models.Node.objects.aget(
                uuid=node_uuid
            )
            script_cell: story_graph_models.ScriptCell = (
                await story_graph_models.ScriptCell.objects.acreate(
                    cell_order=new_script_cell.cell_order,
                    cell_type=new_script_cell.cell_type,
                    cell_code=new_script_cell.cell_code,
                    node=node,
                )
            )
        except Exception as e:
            raise Exception(f"Could not create node: {e}")
        return ScriptCell(
            uuid=script_cell.uuid,
            node=script_cell.node,
            cell_order=script_cell.cell_order,
            cell_code=script_cell.cell_code,
            cell_type=script_cell.cell_type,
        )  # type: ignore

    @strawberry.mutation
    async def update_script_cells(self, info, new_cells: List[ScriptCellInput]) -> None:
        """Updates a given :class:`~story_graph.models.ScriptCell` to change its content."""
        await graphql_check_authenticated(info)
        await sync_to_async(_update_cells)(new_cells)

    @strawberry.mutation
    async def delete_script_cell(self, info, script_cell_uuid: uuid.UUID) -> None:
        """Deletes a given :class:`~story_graph.models.ScriptCell`."""
        await graphql_check_authenticated(info)

        await story_graph_models.ScriptCell.objects.filter(
            uuid=script_cell_uuid
        ).adelete()
        return


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
