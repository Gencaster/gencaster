import asyncio
import uuid
from typing import AsyncGenerator, List

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

from .distributor import GenCasterChannel, GraphUpdateMessage


class AuthStrawberryDjangoField(StrawberryDjangoField):
    def resolver(self, info: Info, source, **kwargs):
        request: HttpRequest = info.context.request
        if not request.user.is_authenticated:
            raise PermissionDenied()
        return super().resolver(info, source, **kwargs)


# this would be better a decorator but strawberry is not nice in these regards, see
# https://stackoverflow.com/a/72796313/3475778
async def graphql_check_authenticated(info: Info):
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
    stream_point: StreamPoint = AuthStrawberryDjangoField()
    stream_points: List[StreamPoint] = AuthStrawberryDjangoField()
    graphs: List[Graph] = AuthStrawberryDjangoField()
    graph: Graph = AuthStrawberryDjangoField()
    nodes: List[Node] = AuthStrawberryDjangoField()
    node: Node = AuthStrawberryDjangoField()


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_node(self, info: Info, new_node: NodeCreate) -> None:
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

        await GenCasterChannel.send_graph_update(
            layer=info.context.channel_layer,
            graph_uuid=graph.uuid,
        )

        return None

    @strawberry.mutation
    async def update_node(self, info: Info, node_update: NodeUpdate) -> None:
        await graphql_check_authenticated(info)

        node = await story_graph_models.Node.objects.select_related("graph").aget(
            uuid=node_update.uuid
        )

        for field in ["position_x", "position_y", "color", "name"]:
            if new_value := getattr(node_update, field):
                setattr(node, field, new_value)

        await sync_to_async(node.save)()

        await GenCasterChannel.send_graph_update(
            layer=info.context.channel_layer,
            graph_uuid=node.graph.uuid,
        )

        return None

    @strawberry.mutation
    async def add_edge(self, info: Info, new_edge: EdgeInput) -> None:
        await graphql_check_authenticated(info)
        in_node: story_graph_models.Node = await sync_to_async(
            story_graph_models.Node.objects.select_related("graph").get
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
        await GenCasterChannel.send_graph_update(
            layer=info.context.channel_layer,
            graph_uuid=in_node.graph.uuid,
        )
        return None

    @strawberry.mutation
    async def delete_edge(self, info, edge_uuid: uuid.UUID) -> None:
        await graphql_check_authenticated(info)
        try:
            edge: story_graph_models.Edge = await sync_to_async(
                story_graph_models.Edge.objects.select_related("in_node__graph").get
            )(uuid=edge_uuid)
            await sync_to_async(edge.delete)()
        except Exception:
            raise Exception(f"Could not delete edge {edge_uuid}")
        await GenCasterChannel.send_graph_update(
            layer=info.context.channel_layer,
            graph_uuid=edge.in_node.graph.uuid,
        )
        return None

    @strawberry.mutation
    async def delete_node(self, info, node_uuid: uuid.UUID) -> None:
        await graphql_check_authenticated(info)
        try:
            node: story_graph_models.Node = await sync_to_async(
                story_graph_models.Node.objects.select_related("graph").get
            )(uuid=node_uuid)
            await sync_to_async(node.delete)()
        except Exception:
            raise Exception(f"Could delete node {node_uuid}")
        await GenCasterChannel.send_graph_update(
            layer=info.context.channel_layer,
            graph_uuid=node.graph.uuid,
        )
        return None

    @strawberry.mutation
    async def add_script_cell(
        self,
        info,
        node_uuid: uuid.UUID,
        new_script_cell: NewScriptCellInput,
    ) -> ScriptCell:
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
        await graphql_check_authenticated(info)
        await sync_to_async(_update_cells)(new_cells)

    @strawberry.mutation
    async def delete_script_cell(self, info, script_cell_uuid: uuid.UUID) -> None:
        await graphql_check_authenticated(info)

        await story_graph_models.ScriptCell.objects.filter(
            uuid=script_cell_uuid
        ).adelete()
        return

    @strawberry.mutation
    async def test_something(self, info: Info, graph_uuid: uuid.UUID) -> None:
        print(info.context.channel_layer)
        await GenCasterChannel.send_message(
            layer=info.context.channel_layer, message=GraphUpdateMessage(graph_uuid)
        )


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 100) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)

    @strawberry.subscription
    async def graph(
        self,
        info: Info,
        graph_uuid: uuid.UUID,
    ) -> AsyncGenerator[Graph, None]:
        graph = await story_graph_models.Graph.objects.aget(uuid=graph_uuid)
        yield graph  # type: ignore

        async for graph_update in GenCasterChannel.receive_graph_updates(
            info.context.ws, graph_uuid
        ):
            yield await story_graph_models.Graph.objects.aget(uuid=graph_update.uuid)  # type: ignore


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)
