import asyncio
from typing import AsyncGenerator, List

import strawberry

from story_graph.tyes import Graph
from stream.types import StreamPoint


@strawberry.type
class Query:
    stream_point: StreamPoint = strawberry.django.field()
    stream_points: List[StreamPoint] = strawberry.django.field()
    graphs: List[Graph] = strawberry.django.field()


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 100) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)


schema = strawberry.Schema(query=Query, subscription=Subscription)
