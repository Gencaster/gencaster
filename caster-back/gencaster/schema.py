import uuid
from typing import List

import strawberry
import strawberry.django
from asgiref.sync import sync_to_async
from django.core.exceptions import PermissionDenied
from django.http.request import HttpRequest
from strawberry.types import Info
from strawberry_django.fields.field import StrawberryDjangoField

import story_graph.models as story_graph_models
from story_graph.types import EdgeInput, Graph, Node, NodeInput, NodeUpdate
from stream.types import StreamPoint


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
    async def add_node(self, info: Info, new_node: NodeInput) -> None:
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
        await graphql_check_authenticated(info)

        node = await story_graph_models.Node.objects.aget(uuid=node_update.uuid)

        for field in ["position_x", "position_y", "color", "name"]:
            if new_value := getattr(node_update, field):
                setattr(node, field, new_value)

        await sync_to_async(node.save)()

        return None

    @strawberry.mutation
    async def add_edge(self, info: Info, new_edge: EdgeInput) -> None:
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
        await graphql_check_authenticated(info)
        try:
            node = await sync_to_async(story_graph_models.Node.objects.get)(
                uuid=node_uuid
            )
            await sync_to_async(node.delete)()
        except Exception:
            raise Exception(f"Could delete node {node_uuid}")
        return None


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
