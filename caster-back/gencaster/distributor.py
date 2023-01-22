import logging
import uuid
from dataclasses import asdict, dataclass, field
from typing import AsyncGenerator, List, Union

from channels.layers import InMemoryChannelLayer
from strawberry.channels import GraphQLWSConsumer

log = logging.getLogger(__name__)


def uuid_to_group(u: uuid.UUID) -> str:
    """Channel group names are not allow
    to have ``-``, so we replace them with ``_``.
    """
    return str(u).replace("-", "_")


class MissingChannelLayer(Exception):
    pass


class GenCasterChannel:
    """
    Abstraction layer for channels.

    Publish and subscribe to specific updates or more general ones as well.
    """

    GRAPH_UPDATE_TYPE = "graph.update"
    NODE_UPDATE_TYPE = "node.update"

    def __init__(self) -> None:
        pass

    @staticmethod
    async def send_graph_update(layer: InMemoryChannelLayer, graph_uuid: uuid.UUID):
        return await GenCasterChannel.send_message(
            layer=layer,
            message=GraphUpdateMessage(uuid=graph_uuid),
        )

    @staticmethod
    async def send_node_update(layer: InMemoryChannelLayer, node_uuid: uuid.UUID):
        return await GenCasterChannel.send_message(
            layer=layer, message=NodeUpdateMessage(uuid=node_uuid)
        )

    @staticmethod
    async def send_message(
        layer: InMemoryChannelLayer,
        message: Union["GraphUpdateMessage", "NodeUpdateMessage"],
    ):
        for channel in message.channels:
            await layer.group_send(channel, asdict(message))

    @staticmethod
    async def receive_graph_updates(
        consumer: GraphQLWSConsumer, graph_uuid: uuid.UUID
    ) -> AsyncGenerator["GraphUpdateMessage", None]:
        group_name = uuid_to_group(graph_uuid)
        if not consumer.channel_layer:
            raise MissingChannelLayer()
        await consumer.channel_layer.group_add(group_name, consumer.channel_name)
        async for message in consumer.channel_listen(
            GenCasterChannel.GRAPH_UPDATE_TYPE, groups=[group_name]
        ):
            yield GraphUpdateMessage(**message)

    @staticmethod
    async def receive_node_updates(
        consumer: GraphQLWSConsumer,
        node_uuid: uuid.UUID,
    ) -> AsyncGenerator["NodeUpdateMessage", None]:
        group_name = uuid_to_group(node_uuid)
        if not consumer.channel_layer:
            raise MissingChannelLayer()
        await consumer.channel_layer.group_add(group_name, consumer.channel_name)
        async for message in consumer.channel_listen(
            GenCasterChannel.NODE_UPDATE_TYPE,
            groups=[group_name],
        ):
            yield NodeUpdateMessage(**message)


@dataclass
class GraphUpdateMessage:
    uuid: uuid.UUID
    type: str = GenCasterChannel.GRAPH_UPDATE_TYPE
    additional_channels: List[str] = field(default_factory=list)

    @property
    def channels(self) -> List[str]:
        return [uuid_to_group(self.uuid)] + self.additional_channels


@dataclass
class NodeUpdateMessage:
    uuid: uuid.UUID
    type: str = GenCasterChannel.NODE_UPDATE_TYPE
    additional_channels: List[str] = field(default_factory=list)

    @property
    def channels(self) -> List[str]:
        return [uuid_to_group(self.uuid)] + self.additional_channels
