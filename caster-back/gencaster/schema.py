import asyncio
import uuid
from typing import AsyncGenerator, List

import strawberry
import strawberry.django
from asgiref.sync import sync_to_async

import story_graph.models as story_graph_models
from story_graph.types import EdgeInput, Graph, Node, NodeInput
from stream.types import StreamPoint


@strawberry.type
class Query:
    stream_point: StreamPoint = strawberry.django.field()
    stream_points: List[StreamPoint] = strawberry.django.field()
    graphs: List[Graph] = strawberry.django.field()
    graph: Graph = strawberry.django.field()
    nodes: List[Node] = strawberry.django.field()
    node: Node = strawberry.django.field()


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_node(self, info, new_node: NodeInput) -> None:
        graph = await sync_to_async(story_graph_models.Graph.objects.get)(
            uuid=new_node.graph_uuid
        )
        node = await sync_to_async(story_graph_models.Node.objects.create)(
            name=new_node.name, graph=graph
        )
        print("Created new node ", node)
        return None

    @strawberry.mutation
    async def add_edge(self, info, new_edge: EdgeInput) -> None:
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
        print("Created new edge ", edge)
        return None

    @strawberry.mutation
    async def delete_edge(self, info, edge_uuid: uuid.UUID) -> None:
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
        try:
            node = await sync_to_async(story_graph_models.Node.objects.get)(
                uuid=node_uuid
            )
            await sync_to_async(node.delete)()
        except Exception:
            raise Exception(f"Could delete node {node_uuid}")
        return None


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 100) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)
