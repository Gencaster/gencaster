import asyncio
from typing import AsyncGenerator, List

import strawberry
import strawberry.django

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
        print(new_node)
        graph = story_graph_models.Graph.objects.get(uuid=new_node.graph_uuid)
        story_graph_models.Node.objects.create(name=new_node.name, graph=graph)
        return None

    @strawberry.mutation
    async def add_edge(self, new_edge: EdgeInput) -> Graph:
        print(new_edge)
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
