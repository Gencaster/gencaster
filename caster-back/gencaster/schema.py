"""
Schema
======

Here we define all the endpoints for GraphQL.

For a specific details of the types consider the
`GraphiQL <https://github.com/graphql/graphiql>`_
page available under the `/graphql` endpoint of
the running backend.
"""

import asyncio
import json
import logging
import os
import uuid
from typing import Any, AsyncGenerator, Dict, List, Optional

import strawberry
import strawberry.django
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User as UserModel
from django.core.exceptions import PermissionDenied
from django.core.files import File
from django.http.request import HttpRequest
from strawberry import auto
from strawberry.types import Info
from strawberry_django.fields.field import StrawberryDjangoField

import story_graph.models as story_graph_models
import stream.models as stream_models
from story_graph.engine import Engine
from story_graph.types import (
    AddGraphInput,
    AudioCellInput,
    EdgeInput,
    Graph,
    GraphFilter,
    Node,
    NodeCreate,
    NodeUpdate,
    ScriptCell,
    ScriptCellInput,
)
from stream.exceptions import NoStreamAvailableException
from stream.types import (
    AddAudioFile,
    AudioFile,
    AudioFileUploadResponse,
    InvalidAudioFile,
    NoStreamAvailable,
    StreamInfo,
    StreamInfoResponse,
    StreamPoint,
    StreamVariable,
    StreamVariableInput,
)

from .distributor import GenCasterChannel, GraphQLWSConsumerInjector

log = logging.getLogger(__name__)


class IsAuthenticated(strawberry.BasePermission):
    message = "User is not authenticated"

    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        if await sync_to_async(lambda: info.context.request.user.is_authenticated)():
            return True
        return False


class AuthStrawberryDjangoField(StrawberryDjangoField):
    """Allows us to restrict certain actions to logged in users."""

    def resolver(self, info: Info, source, **kwargs):
        request: HttpRequest = info.context.request
        if not request.user.is_authenticated:
            raise PermissionDenied()
        return super().resolver(info, source, **kwargs)


async def graphql_check_authenticated(info: Info):
    """Helper function to determine if we are loggin in an async manner.

    This would be better a decorator but strawberry is not nice in these regards, see
    `Stack Overflow <https://stackoverflow.com/a/72796313/3475778>`_.
    """
    auth = await sync_to_async(lambda: info.context.request.user.is_authenticated)()
    if auth is False:
        raise PermissionDenied()


async def update_or_create_audio_cell(
    audio_cell_input: Optional[AudioCellInput],
) -> Optional[story_graph_models.AudioCell]:
    if audio_cell_input:
        (
            audio_cell,
            created,
        ) = await story_graph_models.AudioCell.objects.aupdate_or_create(
            uuid=audio_cell_input.uuid,
            defaults={
                "playback": audio_cell_input.playback,
                "audio_file_id": audio_cell_input.audio_file.uuid,
                "volume": audio_cell_input.volume,
            },
        )
        if created:
            # @todo access .uuid directly to avoid fk access
            # in async mode
            log.debug(f"Created audio cell {audio_cell.uuid}")
    else:
        audio_cell = None
    return audio_cell


@strawberry.django.type(UserModel)
class User:
    username: auto
    is_staff: auto
    is_active: auto
    first_name: auto
    last_name: auto
    email: auto


@strawberry.type
class Query:
    """Queries for Gencaster."""

    stream_point: StreamPoint = strawberry.django.field()
    stream_points: List[StreamPoint] = strawberry.django.field()
    graphs: List[Graph] = strawberry.django.field(filters=GraphFilter)
    graph: Graph = AuthStrawberryDjangoField()
    nodes: List[Node] = AuthStrawberryDjangoField()
    node: Node = AuthStrawberryDjangoField()
    audio_files: List[AudioFile] = AuthStrawberryDjangoField()
    audio_file: AudioFile = AuthStrawberryDjangoField()
    stream_variable: StreamVariable = AuthStrawberryDjangoField()

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def is_authenticated(self, info) -> User:
        return info.context.request.user  # type: ignore


@strawberry.type
class Mutation:
    """Mutations for Gencaster via GraphQL."""

    @strawberry.mutation
    async def add_node(self, info: Info, new_node: NodeCreate) -> None:
        """Creates a new :class:`~story_graph.models.Node` in a given
        ~class:`~story_graph.models.Graph`.
        Although it creates a new node with UUID we don't hand it back yet.
        """
        await graphql_check_authenticated(info)

        graph = await story_graph_models.Graph.objects.aget(uuid=new_node.graph_uuid)
        node = story_graph_models.Node(
            name=new_node.name,
            graph=graph,
        )

        # transfer from new_node to node model if attribute is not none
        for field in ["position_x", "position_y", "color"]:
            if new_value := getattr(new_node, field):
                setattr(node, field, new_value)

        # asave not yet implemented in django 4.1
        await sync_to_async(node.save)()

        await GenCasterChannel.send_graph_update(
            layer=info.context.channel_layer,
            graph_uuid=graph.uuid,
        )

        return None

    @strawberry.mutation
    async def update_node(self, info: Info, node_update: NodeUpdate) -> None:
        """Updates a given :class:`~story_graph.models.Node` which can be used
        for renaming or moving it across the canvas.
        """
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

        await GenCasterChannel.send_node_update(
            layer=info.context.channel_layer,
            node_uuid=node.uuid,
        )

        return None

    @strawberry.mutation
    async def add_edge(self, info: Info, new_edge: EdgeInput) -> None:
        """Creates a :class:`~story_graph.models.Edge` for a given
        :class:`~story_graph.models.Graph`.
        It does not return the created edge.
        """
        await graphql_check_authenticated(info)
        in_node: story_graph_models.Node = (
            await story_graph_models.Node.objects.select_related("graph").aget(
                uuid=new_edge.node_in_uuid
            )
        )
        out_node: story_graph_models.Node = await story_graph_models.Node.objects.aget(
            uuid=new_edge.node_out_uuid
        )
        edge: story_graph_models.Edge = await story_graph_models.Edge.objects.acreate(
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
        """Deletes a given :class:`~story_graph.models.Edge`."""
        await graphql_check_authenticated(info)
        try:
            edge: story_graph_models.Edge = (
                await story_graph_models.Edge.objects.select_related(
                    "in_node__graph"
                ).aget(uuid=edge_uuid)
            )
            await story_graph_models.Edge.objects.filter(uuid=edge_uuid).adelete()
        except Exception:
            raise Exception(f"Could not delete edge {edge_uuid}")
        await GenCasterChannel.send_graph_update(
            layer=info.context.channel_layer,
            graph_uuid=edge.in_node.graph.uuid,
        )
        return None

    @strawberry.mutation
    async def delete_node(self, info, node_uuid: uuid.UUID) -> None:
        """Deletes a given :class:`~story_graph.models.Node`."""
        await graphql_check_authenticated(info)
        try:
            node: story_graph_models.Node = (
                await story_graph_models.Node.objects.select_related("graph").aget(
                    uuid=node_uuid
                )
            )
            await story_graph_models.Node.objects.filter(uuid=node_uuid).adelete()
        except Exception:
            raise Exception(f"Could delete node {node_uuid}")

        await GenCasterChannel.send_graph_update(
            layer=info.context.channel_layer,
            graph_uuid=node.graph.uuid,
        )

        await GenCasterChannel.send_node_update(
            layer=info.context.channel_layer,
            node_uuid=node.uuid,
        )

        return None

    @strawberry.mutation
    async def create_update_script_cells(
        self, info, script_cell_inputs: List[ScriptCellInput], node_uuid: uuid.UUID
    ) -> List[ScriptCell]:
        """Creates or updates a given :class:`~story_graph.models.ScriptCell` to change its content."""
        await graphql_check_authenticated(info)

        try:
            node: story_graph_models.Node = await story_graph_models.Node.objects.aget(
                uuid=node_uuid
            )
        except story_graph_models.Node.DoesNotExist as e:
            log.error(f"Received update on unknown node {node_uuid}")
            # @todo return error
            raise e

        script_cells: List[story_graph_models.ScriptCell] = []

        for script_cell_input in script_cell_inputs:
            audio_cell = await update_or_create_audio_cell(script_cell_input.audio_cell)

            # if no cell order is given we add it to the end of the current node
            if not script_cell_input.cell_order:
                cur_max_cell_order = (
                    await story_graph_models.ScriptCell.objects.filter(node=node)
                    .order_by("-cell_order")
                    .afirst()
                )
                if cur_max_cell_order:
                    script_cell_input.cell_order = cur_max_cell_order.cell_order + 1
                else:
                    script_cell_input.cell_order = 0

            (
                script_cell,
                created,
            ) = await story_graph_models.ScriptCell.objects.aupdate_or_create(
                uuid=script_cell_input.uuid,
                defaults={
                    "cell_order": script_cell_input.cell_order,
                    "cell_type": script_cell_input.cell_type,
                    "cell_code": script_cell_input.cell_code,
                    "node": node,
                    "audio_cell": audio_cell,
                },
            )
            if created:
                log.debug(f"Created script cell {script_cell.uuid}")

            script_cells.append(script_cell)

        await GenCasterChannel.send_node_update(
            layer=info.context.channel_layer, node_uuid=node.uuid
        )
        return script_cells  # type: ignore

    @strawberry.mutation
    async def delete_script_cell(self, info, script_cell_uuid: uuid.UUID) -> None:
        """Deletes a given :class:`~story_graph.models.ScriptCell`."""
        await graphql_check_authenticated(info)

        # first get the node before the cell is deleted
        node = await story_graph_models.Node.objects.filter(
            script_cells__uuid=script_cell_uuid
        ).afirst()

        await story_graph_models.ScriptCell.objects.filter(
            uuid=script_cell_uuid
        ).adelete()

        if node:
            await GenCasterChannel.send_node_update(
                layer=info.context.channel_layer,
                node_uuid=node.uuid,
            )

    @strawberry.mutation
    async def add_graph(self, info, graph_input: AddGraphInput) -> Graph:
        await graphql_check_authenticated(info)

        graph = await story_graph_models.Graph.objects.acreate(
            name=graph_input.name,
        )
        await graph.acreate_entry_node()
        # need a refresh - in django 4.2 this will be available, see
        # https://docs.djangoproject.com/en/4.2/ref/models/instances/#django.db.models.Model.arefresh_from_db
        return await story_graph_models.Graph.objects.aget(uuid=graph.uuid)  # type: ignore

    @strawberry.mutation
    async def add_audio_file(self, info, new_audio_file: AddAudioFile) -> AudioFileUploadResponse:  # type: ignore
        if new_audio_file.file is None or len(new_audio_file.file) == 0:
            return InvalidAudioFile(error="Received empty audio file")
        elif not os.path.splitext(new_audio_file.file_name)[-1].lower() in [
            ".flac",
            ".wav",
        ]:
            return InvalidAudioFile(error="Only support flac and wav files")
        try:
            audio_file = await stream_models.AudioFile.objects.acreate(
                name=new_audio_file.name,
                file=File(new_audio_file.file, name=new_audio_file.file_name),
                description=new_audio_file.description,
                auto_generated=False,
            )
        except Exception as e:
            return InvalidAudioFile(
                error=f"Unexpected error, could not save audio file: {e}"
            )
        return audio_file

    @strawberry.mutation
    async def create_update_stream_variable(
        self, info, stream_variables: List[StreamVariableInput]
    ) -> List[StreamVariable]:
        stream_vars: List[stream_models.StreamVariable] = []

        for stream_variable in stream_variables:
            (
                stream_var,
                _,
            ) = await stream_models.StreamVariable.objects.aupdate_or_create(
                stream=await stream_models.Stream.objects.aget(
                    uuid=stream_variable.stream_uuid
                ),
                key=stream_variable.key,
                defaults={
                    "value": stream_variable.value,
                    "stream_to_sc": stream_variable.stream_to_sc,
                },
            )
            if stream_variable.stream_to_sc:
                await sync_to_async(stream_var.send_to_sc)()
            stream_vars.append(stream_var)

        return stream_vars  # type: ignore


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

    @strawberry.subscription
    async def node(
        self,
        info: Info,
        node_uuid: uuid.UUID,
    ) -> AsyncGenerator[Node, None]:
        node = await story_graph_models.Node.objects.aget(uuid=node_uuid)
        yield node  # type: ignore

        async for node_update in GenCasterChannel.receive_node_updates(
            info.context.ws, node_uuid
        ):
            yield await story_graph_models.Node.objects.aget(uuid=node_update.uuid)  # type: ignore

    @strawberry.subscription
    async def stream_info(
        self,
        info: Info,
        graph_uuid: uuid.UUID,
    ) -> AsyncGenerator[StreamInfoResponse, None]:  # type: ignore
        consumer: GraphQLWSConsumerInjector = info.context.ws

        graph = await story_graph_models.Graph.objects.filter(uuid=graph_uuid).afirst()
        if not graph:
            raise Exception("could not find graph!")

        try:
            stream = await stream_models.Stream.objects.aget_free_stream(graph)
        except NoStreamAvailableException:
            yield NoStreamAvailable()
            return

        await stream.increment_num_listeners()

        engine = Engine(
            graph=graph,
            stream=stream,
        )

        async def cleanup():
            await stream.decrement_num_listeners()

        async def cleanup_on_stop(**kwargs: Dict[str, str]):
            """
            A helper function which scans for a "stop" signal send via the websocket connection of our
            graphql subscription as this is the indication from urql that we paused the subscription.
            """
            if text_data := kwargs.get("text_data"):
                d = json.loads(text_data)  # type: ignore
                if d.get("type") == "stop":
                    log.info("Stop a stream due to a stop signal")
                    await cleanup()

        consumer.disconnect_callback = cleanup
        consumer.receive_callback = cleanup_on_stop

        async for instruction in engine.start(max_steps=int(10e4)):
            yield StreamInfo(
                stream=stream,  # type: ignore
                stream_instruction=instruction,  # type: ignore
            )


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)
