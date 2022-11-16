import asyncio

from stream.models import StreamPoint

from .models import Graph, Node


class Engine:
    def __init__(self, graph: Graph, streaming_point: StreamPoint) -> None:
        self.graph: Graph = graph
        self.streaming_point = streaming_point
        self._current_node: Node

    async def start(self):
        if new_node := await self.graph.get_entry_node():
            self._current_node = new_node
        else:
            print("Could not find entry node :/")
            return

        for _ in range(10):
            print(self._current_node)
            if (
                new_node := await Node.objects.filter(
                    out_edges__out_node=self._current_node
                )
                .order_by("?")
                .afirst()
            ):
                self._current_node = new_node
            else:
                print("Got nowhere to go?")
            await asyncio.sleep(0.5)
