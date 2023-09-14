"""
Distributor
===========

A collection of async messaging tools which is used by our GraphQL schema.

"""

import logging
import uuid
from dataclasses import asdict, dataclass, field
from typing import AsyncGenerator, Awaitable, Callable, List, Optional, Union

from channels.layers import get_channel_layer
from channels_redis.core import RedisChannelLayer
from strawberry.channels import GraphQLWSConsumer

log = logging.getLogger(__name__)


def uuid_to_group(u: Union[uuid.UUID, str]) -> str:
    """Channel group names are not allow
    to have ``-``, so we replace them with ``_``.
    """
    return str(u).replace("-", "_")


class MissingChannelLayer(Exception):
    pass


class GraphQLWSConsumerInjector(GraphQLWSConsumer):
    """Allows us to inject callbacks on e.g. a disconnect.

    .. todo::

        This can be made obsolete via
        https://github.com/strawberry-graphql/strawberry/pull/2430

    """

    def __init__(self, *args, **kwargs):
        self.disconnect_callback: Optional[Callable[[], Awaitable[None]]] = None
        self.receive_callback: Optional[Callable] = None
        super().__init__(*args, **kwargs)

    async def websocket_disconnect(self, message):
        if self.disconnect_callback:
            await self.disconnect_callback()
        return await super().websocket_disconnect(message)

    async def receive(self, *args, **kwargs) -> None:
        if self.receive_callback:
            await self.receive_callback(*args, **kwargs)
        await super().receive(*args, **kwargs)


class GenCasterChannel:
    """
    Abstraction layer for channels.

    Publish and subscribe to specific updates or more general ones as well.
    """

    GRAPH_UPDATE_TYPE = "graph.update"
    NODE_UPDATE_TYPE = "node.update"
    STREAM_LOG_UPDATE_TYPE = "stream_log.update"
    STREAMS_UPDATE_TYPE = "streams.update"

    def __init__(self) -> None:
        pass

    @staticmethod
    def _get_layer() -> RedisChannelLayer:
        if layer := get_channel_layer():
            return layer
        raise Exception("Could not obtain redis channel layer")

    @staticmethod
    async def send_graph_update(graph_uuid: uuid.UUID):
        return await GenCasterChannel.send_message(
            layer=GenCasterChannel._get_layer(),
            message=GraphUpdateMessage(uuid=str(graph_uuid)),
        )

    @staticmethod
    async def send_node_update(node_uuid: uuid.UUID):
        return await GenCasterChannel.send_message(
            layer=GenCasterChannel._get_layer(),
            message=NodeUpdateMessage(uuid=str(node_uuid)),
        )

    @staticmethod
    async def send_log_update(stream_log_message: "StreamLogUpdateMessage"):
        return await GenCasterChannel.send_message(
            layer=GenCasterChannel._get_layer(), message=stream_log_message
        )

    @staticmethod
    async def send_streams_update(stream_uuid: str):
        return await GenCasterChannel.send_message(
            layer=GenCasterChannel._get_layer(),
            message=StreamsUpdateMessage(uuid=str(stream_uuid)),
        )

    @staticmethod
    async def send_message(
        layer: RedisChannelLayer,
        message: Union[
            "GraphUpdateMessage",
            "NodeUpdateMessage",
            "StreamLogUpdateMessage",
            "StreamsUpdateMessage",
        ],
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

    @staticmethod
    async def receive_stream_log_updates(
        consumer: GraphQLWSConsumer,
    ) -> AsyncGenerator["StreamLogUpdateMessage", None]:
        group_name = GenCasterChannel.STREAM_LOG_UPDATE_TYPE
        if not consumer.channel_layer:
            raise MissingChannelLayer()
        await consumer.channel_layer.group_add(group_name, consumer.channel_name)
        async for message in consumer.channel_listen(
            GenCasterChannel.STREAM_LOG_UPDATE_TYPE,
            groups=[group_name],
        ):
            yield StreamLogUpdateMessage(**message)

    @staticmethod
    async def receive_streams_updates(
        consumer: GraphQLWSConsumer,
    ) -> AsyncGenerator["StreamsUpdateMessage", None]:
        group_name = GenCasterChannel.STREAMS_UPDATE_TYPE
        if not consumer.channel_layer:
            raise MissingChannelLayer()
        await consumer.channel_layer.group_add(group_name, consumer.channel_name)
        async for message in consumer.channel_listen(
            GenCasterChannel.STREAMS_UPDATE_TYPE,
            groups=[group_name],
        ):
            yield StreamsUpdateMessage(**message)


@dataclass
class GraphUpdateMessage:
    # we can not transfer an UUID via redis so we encode it as string early
    uuid: str
    type: str = GenCasterChannel.GRAPH_UPDATE_TYPE
    additional_channels: List[str] = field(default_factory=list)

    @property
    def channels(self) -> List[str]:
        return [uuid_to_group(self.uuid)] + self.additional_channels


@dataclass
class NodeUpdateMessage:
    uuid: str
    type: str = GenCasterChannel.NODE_UPDATE_TYPE
    additional_channels: List[str] = field(default_factory=list)

    @property
    def channels(self) -> List[str]:
        return [uuid_to_group(self.uuid)] + self.additional_channels


@dataclass
class StreamLogUpdateMessage:
    # todo if a str is inserted here it will fail
    uuid: str
    stream_point_uuid: Optional[str]
    stream_uuid: Optional[str]

    type: str = GenCasterChannel.STREAM_LOG_UPDATE_TYPE

    additional_channels: List[str] = field(default_factory=list)

    @property
    def channels(self) -> List[str]:
        return [GenCasterChannel.STREAM_LOG_UPDATE_TYPE] + self.additional_channels


@dataclass
class StreamsUpdateMessage:
    uuid: str

    type: str = GenCasterChannel.STREAMS_UPDATE_TYPE

    additional_channels: List[str] = field(default_factory=list)

    @property
    def channels(self) -> List[str]:
        return [GenCasterChannel.STREAMS_UPDATE_TYPE] + self.additional_channels
