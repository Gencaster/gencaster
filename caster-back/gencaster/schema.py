from typing import List

import strawberry

from stream.types import StreamPoint


@strawberry.type
class Query:
    stream_point: StreamPoint = strawberry.django.field()
    stream_points: List[StreamPoint] = strawberry.django.field()


schema = strawberry.Schema(query=Query)
