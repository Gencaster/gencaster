from typing import List

import strawberry

from story_graph.tyes import Graph
from stream.types import StreamPoint


@strawberry.type
class Query:
    stream_point: StreamPoint = strawberry.django.field()
    stream_points: List[StreamPoint] = strawberry.django.field()
    graphs: List[Graph] = strawberry.django.field()


schema = strawberry.Schema(query=Query)
